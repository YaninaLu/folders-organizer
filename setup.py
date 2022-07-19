from setuptools import setup


setup(name="clean_folder",
      version="1.0",
      description="Folder organizer",
      url="https://github.com/YaninaLu/folders-organizer",
      author="Yanina Lubenska",
      author_email="yaninaosadchaya@gmail.com",
      packages=["clean_folder"],
      entry_points={"console_scripts": ["clean-folder = clean_folder.clean:clean_folder"]}
      )
