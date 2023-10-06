# 2023 NFL ML/DS/DE Project Sandbox
#### by Samuel Sisk
###
###
JIRA - https://ssisk44.atlassian.net/jira/software/projects/BH2023/boards/1/timeline?timeline=WEEKS

# Objectives
1) Create flawless pipelines to collect and store sets of NFL data
2) Design methods for various data acquisition and manipulation requirements
3) Train models
4) Engineer a system for testing/training analysis methods on historical data


## Project Introduction
As I currently take the beginning steps in my third attempt to perfect my sports betting prediction skills, I realize how far I have come both as a programmer and active thinker.
Just three years ago during my final year in college, did I believe that one man could intake and decipher the information required to outperform a computer. An honest man's mistake,
fortunately my thumb twiddling had been done with quarters and not life altering amounts of money. Thought each year I continually perform better, I still lose a small amount of money.

####Things I Have Learned About Gambling
1) The house always wins
2) In non-chance based games, innovation that produces success is rewarded

####Things I Have Observed But Do Not Know Be True
1) New gambling companies and methods are most likely sloppier and more likely to have a higher return to customers to gain traction
2) Anyone who develops more accurate methods can do one of two things
   1) Profit off of less accurate methods used by odds makers
   2) Sell the superior method to the house
   
####What Makes Fantasy Sports Lineup Betting Unique
The chances of drawing a spade from a full deck of cards is 25%. This is a purely mathematical game with perfectly known odds, the result of an individuals' performance in a sporting match
is not. The result of an individuals efforts in a sporting match are far less cut and dry. While attempting to predict the reality that truly unfolds among the many ephemeral futures
is not a game of chance, there are many mathematical constructs that lay the foundation for the flow and results of a football game.

Unfortunately, many large corporations for traditional betting forms have teams of advanced mathematicians and programmers that upkeep their odds to ensure maximum profit. Fortunately fantasy
betting actually places the entries into a pool to compete amongst each other. This different is incredibly important because it is no longer a priority for the company to see success in the
competition itself. Corporations like FanDuel and DraftKings take a flat cut of the prize money before diving it amongst the winners. The winners in fantasy sports are the predetermined proportion
of entries to score into a certain percentile. Different contests have different payout structures. For example, the contest I most recently participated in was a $5 buy in to a $1.6 million dollar
prize pool payout with a total 354,000 entries. The last spot to get the minimum payout of $9 was place 88,346. This minimum winner slot scored 127.92 points while the overall winner put up a 
cool 225.38. 

Now what does any of that mean. It means that out of the people who entered, only about 24.95% of people won money. The average players bet was immediately worth $4.52(((entry_fee*num_entered)-prize_payout)/num_entered) after paying a $0.48 fee per entry 
to Fanduel. The average winner won $14.72(prize_payout/num_payouts), making only $9.72 from the bet. From that we can see the average amount won (avg_win/(1/win_percent)) for each entry is $3.67. Which means you would need
an expected winning percent ((avg_win/x) = 5 and win_percent=(1/(1-x))) of 34% to break even on each attempted entry. While I think that a MINIMUM 9.05% edge is near impossible against traditional enterprises, gaining that
on the average betting human might not be as hard. The 9.05% edge does not account for the fact that the winner prize pool increases exponentially thus skewing the average winners' payout slight up.

 
### Thesis
I believe that using advanced computational methods for fantasy sports betting represents a (1) semi-competitive, (2) achievable, (3) profitable personal income stream. In order to do this I plan on
designing data relationships in logical systems that improve the computational understanding of the fundamental real life aspects of football. Human nature and performance is pattern based, the difficulty
here is that reality often translates poorly to computer data representations.











###
## The Purpose and Intention Behind This Project ##
Figma - https://www.figma.com/file/EJoeKfV4QVjThu3oXcM2YD/2023-ML-Injection-into-DFS-Project-Overview?type=whiteboard&node-id=904-177&t=OdMaRGOZrR9U2E0s-0
###
## Coding Standards
- ***Folder*** names should all capitalized and underscore spacing
  - Folder
  - Folder_Name
####
- ***File***, ***Method***, and ***Variable*** names should be camel case with all but the first word capitalized
  - fileNameExample.py
  - def methodNameExample():
  - variableNameExample = 0


###
## Simple NFL ML Game Score Prediction Project
- design a system for acquiring/deciphering franchise name, team name, and team abbreviation for each season

###
## Maintenance Notes
Incorporate a research mode feature with a team or players dashboard stats - https://www.teamrankings.com/nfl/stats/