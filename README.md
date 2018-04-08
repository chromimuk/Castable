Small Python program that will generates an HTML page containing all the videos from a folder.
Opened with Chrome, the page will make an easy-to-use interface to stream the videos to local Chomecast devices.

I had several interesting challenges working on it:
* managing a local server for the Chromecast devices to ba able to read the videos ;
* taking care of all the possible actions of a player (play, pause, stop, change video, restart) in a "remote" context (connection/disconnection to the device) ;
* generating a good and usable interface in vanilla Javascript.
