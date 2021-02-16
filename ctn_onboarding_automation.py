import csv
import io
import os
import sys
from threading import Thread

import wx
import wx.lib.newevent

from src.config import Config
from src.person import Person
from src.qualtrics import QualtricsQuery
from src.sheet import Sheet
from src.utils import to_string

# Define notification event for thread updates
ResultEvent, EVT_RESULT = wx.lib.newevent.NewEvent()


# Thread class that executes processing
class WorkerThread(Thread):
    def __init__(self, notify_window):
        """Initialize worker thread."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Run worker thread."""
        wx.PostEvent(self._notify_window, ResultEvent(data="Contacting Qualtrics..."))
        q = QualtricsQuery(config)
        responses = q.get_survey_response()

        f = io.StringIO(responses)
        reader = csv.reader(f)
        wx.PostEvent(self._notify_window, ResultEvent(data="Got all onboarding survey results"))
        try:
            wx.PostEvent(self._notify_window, ResultEvent(data=f'Opening tracking sheet at: {config.get_file_path()}'))
            tracking_sheet = Sheet(config.get_file_path())
        except FileNotFoundError:
            wx.PostEvent(self._notify_window, ResultEvent(data=f'Unable to find the tracking sheet at \'{config.get_file_path()}\''))
            wx.PostEvent(self._notify_window, ResultEvent(data='Could not update sheet'))
            return

        for i, r in enumerate(reader):
            # Skip first five rows
            if i < 5:
                continue
            # for each response, verify that the person is in the workbook. If they are not, add them
            # Columns start counting from 0 (first column is column 0)
            p = Person(first_name=r[17],
                       last_name=r[18],
                       uo_id=r[42],
                       duck_id=r[44],
                       position_type=r[24],
                       supervisor=r[22],
                       confidentiality_date=r[0],
                       era_commons_id=r[46],
                       prox=r[43])
            if not tracking_sheet.find_person(p):
                wx.PostEvent(self._notify_window, ResultEvent(data=f'Updating: {r[18]}'))

                added_date = r[1]
                note = f'Added on {to_string(added_date)}'
                tracking_sheet.add_person(p, note)

        wx.PostEvent(self._notify_window, ResultEvent(data='Completed!'))

    def abort(self):
        """Abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1


# GUI Frame class that spins off the worker thread
class MainFrame(wx.Frame):
    def __init__(self, parent, id):
        """Create the MainFrame."""
        wx.Frame.__init__(self, parent, id, title='CTN Onboarding Automation', size=wx.Size(900, 600))

        # Simple frame with only text
        self.status = wx.StaticText(self, -1, '', pos=(0,100))

        # Set up event handler for any worker thread results
        self.Bind(EVT_RESULT, self.OnResult)

        # And start up the worker thread
        self.worker = WorkerThread(self)

    def OnResult(self, event):
        """Show Result status."""
        # Process results here
        label = self.status.GetLabel()
        label = label + '\n' + event.data
        self.status.SetLabel(f'{label}')
        # In either event, the worker is done
        self.worker = None


class MainApp(wx.App):
    def OnInit(self):
        """Initialize Main App."""
        self.frame = MainFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path = os.path.abspath(os.path.join(bundle_dir, 'config.json'))

    config = Config(path)

    app = MainApp(0)
    app.MainLoop()
