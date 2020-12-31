# import packages
from src.utility.environment import Environment, load_dotenv
from src.resources.main_frame import MainFrame
import os

Environment.base_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv()


if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
