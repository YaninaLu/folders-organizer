# File Sorter

This project takes as input path to the directory that the user wants to sort out.
Then this directory is traversed file by file and when it meets a folder it calls itself 
recursively.

It processes the files in the following way:
- the filename is being normalized by getting rid of non-latin letters and non-alphanumeric symbols
- then the file is moved into one of the folders (images, video, audio, documents, or archives) according to its extension
- archives are not only moved to the "archives" folder but also unpacked into an enclosed folder named after it
- empty folders are deleted

The script returns a list of extensions met in the folder and a list of extensions that it didn't process.
And also a tree of all the folders and files in the organized folder.
