# Who Took a Raptor From the Raptor Jar?
### By Chef J. Pex

## Description:
The players are given `logs.json` and a map of the raptor cages to figure out why raptors have been going missing recently. They must figure out which employee ID belongs to who by checking GM badges. The flag is the name of the employee who is suspected of stealing baby raptors.

## Challenge:

During this past week, baby raptors have been mysteriously going missing. At first, it was attributed to counting errors or the sneaky nature of the babies, but it has been adding up. Something, or someone, is causing these disappearances. Management still hasn't approved increasing our security budget to install CCTV, so all we have to work with are the keycard door logs of the raptor cages and a map of the area.

Using this information, who should be the primary suspect?

## Instructions:

* To solve this challenge, players must create a script to find which employee ID has been entering/exiting the habitat doors the most.
* They will find that the new hire, Nate Ernson (Dino Research Intern), is that person. Upon further analysis, they will find that every time the intern enters/exits a habitat, it had occurred without him entering any previous door.
* Once player realize this, they will find out that employee ID `10C971` always makes trips to the enclosures, then immediately after, the intern's card is swiped into the habitats.
* They should come to the conclusion that employee `10C971` has stolen the intern's keycard to gain access to the habitats.
* They must now come up to each GM and ask to see their badge to figure out which employee is `10C971`. The correct answer is below.
<br>

<details>
<summary>Flag</summary>

`flag{Chef J. Pex}`
</details>