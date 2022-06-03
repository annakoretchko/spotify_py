
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


## spotify_py

This repo uses the Spotify API to automatically add set podcasts to queue at a set time in the morning so that you can wake up to your
daily news podcasts already queued to go. 

## Sources
I used various links to figure out how the Spofity API works. I ended up using a combination of the spotipy python package and the
regular Spotify API Documents

- [Spotify API Walkthrough Example](https://stmorse.github.io/journal/spotify-api.html)
- [Spotify API Documentation](https://developer.spotify.com/documentation/)
- [Python Spotipy Package](https://pypi.org/project/spotipy/)

## Automate The Run

On a Linux/MacOS system you can use [Cron Tab](https://www.geeksforgeeks.org/crontab-in-linux-with-examples/) to run run at a set time. For example, I have the following so that it automatically runs and adds to my queue at 8:30 am on weekdays.

In the terminal:

```
crontab -l 

PATH=/Users/anna/miniforge3/envs/spotify/bin
30 08 * * 1-5 cd ~/Dev/spotify_py/ && python main.py
```

If you are on a Windows machine, you can use a similar tool called [**Task Scheduler**](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10) 

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

* Anna Koretchko - [Personal Website](https://anna-koretchko.ue.r.appspot.com/index)
* Email - annakoretchko@gmail.com

[linkedin-url]: https://www.linkedin.com/in/anna-koretchko-1b5b0211a/
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/annakoretchko/garmin_analysis/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
