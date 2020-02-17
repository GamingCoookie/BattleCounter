# WorldOfTanks-BattleCounter

## Why?

I wrote this program to count how many skirmish battles each of our clan members played together with a given commander. Where before I
had to spend about 2 to 3 hours for 200 battles to write down and count the battles it now only takes 5 seconds. And you could apply this
to other game modes as well. 
But for skirmishes or clan battles in general it makes the most sense because it reflects how many battles the players have actually
played with the clan.
Or you could use it to check how many times you have played with a friend or met someone in the enemy team as it not only checks your team but both teams.

## How do I use this power?

Either open the main.py with at least Python 3.7 or if you are on Windows use the provided WoTBattleCounter.exe in the releases section.

#### Make sure that all the Replays you want to use are complete and you didn't exist the battle prior.

Then you click on "Open skirmish files" and point it to the folder where you have your replays saved. It also checks subfolders so you could have replays
neatly sorted into days, weeks, months and years and just point it at the "month" folder to see how many battles were played by player x in that month.

Then or before the previous step you enter all the names into the list. You do that by clicking on that text entry field and type in a name and press enter
if you want to delete a name from the list, you click in the list on that name and press the "Delete" key on your keyboard.

If you are done I'd recommend saving the list with "Save list" if you want to reuse it and then click on "Count!".

After it's done you'll be able to just read of the names + battle count in the list.

### Important Source that I used

This is made possible all in one program because I used adapted code snippets from [Phalynx's WoT-Replay-To-JSON program](https://github.com/Phalynx/WoT-Replay-To-JSON).
