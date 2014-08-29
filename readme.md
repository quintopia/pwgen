Problem: If I use an easy to remember password, consisting of words and number pre/suffixes, with some letters substituted by similar-looking symbols/numbers, my password is easily crackable by dictionary attack.

Solution: Use a somewhat random string of symbols.

Problem: I can probably memorize a random string of symbols, but only if I use it for every website, but if I do that, I need only to slip up once and fall for a clever phishing attack, and they can log in anywhere I can. Even if I realize my mistake and change the password, I have to go through every other website and change those passwords too!

Solution: Use a different random string of symbols for every website.

Problem: C'mon, man, there's no way I can remember all those random strings without writing them down somewhere, and I'm not 100% sure I can trust my coworkers....

Solution: Use the Bruce Schneier system to generate your random strings, then you only need to remember phrases you probably already have memorized.

Problem: But how the heck am I going to remember which phrase goes with which site? It's still way too much for my feeble human memory.

Solution: Use a deterministic password generator, which turns a password you've already memorized into a different password depending on which site it's going to be used for.

Problem: That's better, but it brings us back to the problem before: a cracker who gets the password I use to generate the different passwords can do the same thing and log in anywhere I can log in.

Solution: Use a deterministic password generator that uses a different easily-memorized code for each website it generates a password for.

Problem: Now we're back at the situation where I have to remember lots of different things, and it doesn't matter if they are all individually memorable, because how am I going to remember which one goes with which site? I can't really see what we've bought here that we didn't have using the Schneier system.

Solution: Since it's always the same piece of software that you're interacting with in this situation, what we've bought is the ability to leverage that central source to provide you with some sort of visual memory prompt. Some websites already do this, though they currently do so in order to prevent phishing attacks. Furthermore, we can have the unique per-website code be related to the memory prompt in some extremely easy-to-remember way.

Problem: Okay, I can see how that will help me remember which one goes with which site, but you're still saying I have to remember a whole bunch of different codes. It's possible I'll just entirely forget one of them, even with the prompt, especially if it's for a site I don't use often.

Question: Some things you just don't forget forget. If someone dropped you in the house you grew up in, could you find your way back to your bedroom? If I dropped you off on the side of the street near the campus of your alma mater, could you find your way to the building where you took your freshman math classes?

Answer: Well, I can remember those thing vividly. I wouldn't even need you to take me there. I can find my way inside my own head just from memory. Couldn't for the life of me tell you how to drive to that one hotel I stayed in that one time in that one town five years ago, though, and I feel like the "rarely used website" fits more in this category than in the "places I spent large portions of my life" category.

Question: But you've admitted that you can remember /places/ very vividly, and in fact, we know that human brains (and brains of other mammals) are especially suited to this kind of memory. What if I placed you in a car on the road that you took to get into that one town. Don't you think you'd recognize enough of it to find your way back there, without even having to guess very much along the way?

Answer: Well, I don't know for sure without trying.

Solution: Nonetheless, many people do find that being in certain places stimulates their memory of things that happened there, and where they were when those things happened, and sometimes even the relationships between those places. But all we actually need to solve your problem is the ability to remember /what happened/ in a particular location upon seeing it, and for a large majority of people, this is the easiest sort of thing to remember. 

So what we need is this: a deterministic password generator that shows you a mock-up of a place, lets you decide what happens there, perhaps by letting you illustrate a story and create an associated memory, and generates a password based on that illustration. Of course, we need the place to always look the same for a given website, but that's not hard: if we're generating passwords, generating places should be no harder. Furthermore, we need to ensure that no two websites generate similar places, but that is again just a technical problem, easily solved by having a large enough variety of landmarks to choose from.

Here's how it could work: A website-specific map is displayed, along with a number of characters and props which you can move around. You decide where to put them based on the story you have in mind, and it generates a password based on where you put them. As long as you always put them in the right place, you get the right password back.

Problem: I think I'm ready to allow that this solution might address all of the problems I've posed so far, except for one: I can't trust my coworkers. If a colorful map appears on the screen and I drag and drop characters to specific places, it's exceedingly easy for a sneaky shoulder-surfer to replicate my actions and get my password. At least with traditional passwords, the screen won't display what I'm typing.

Solution: Easy enough. We just require that you enter a normal password of the traditional type in order for the map to be displayed. If your coworker doesn't know that password, they won't see the map, and they can't generate the same series of actions you did to generate your password. Especially if the generated password also depends on this normal password as well.

Problem: So now you've got me memorizing traditional passwords again?

Solution: Just one! You can use the same password for every website without fear, and you never need change it. We can still generate different maps for each website even if its the same password. And there's another problem with traditional passwords that you never even mentioned: keyloggers. Notice that this system, because the last step of the process is done entirely with the mouse and the clipboard, is entirely immune to them. Of course, if your coworker installs a keylogger to get your master password and then shoulder-surfs surreptitiously to find out what you do with the map, they could get your password. But that's still one more step than they'd need with a traditional password!

Problem: So the password goes through my clipboard...which means that someone could just paste it from there later, right?

Solution: Not if the program wipes the clipboard after a short period of time.

Problem: Still, a malicious process could watch the clipboard and harvest passwords from it?

Solution: You're right, it's probably better to have the password be dragged-and-dropped from the generator, where possible.

Problem: Alright, let's suppose we can work out all the security issues, or be comfortable with the level of security we've achieved. Isn't this all very inconvenient? I mean, what if I need to change my password?

Solution: Bruce Schneier says you should never change your password unless you have good reason to believe it is compromised, or you forget it. Ideally, we're generating passwords secure enough that you may never need to change them. You know, unless you've signed up for a website so insecure it saves your password in plaintext, but we can hope that kind of thing doesn't happen anymore. Either way, changing your password is really easy: Just change the story, drag and drop some character to a different location. And we can make it so that the resulting password is entirely different from the original based on a very small change in the story.

Problem: But wouldn't a lot of websites and other software just reject a totally random password? "You can't use those characters!" or "You MUST use these characters!"

Solution: True, it's silly, but it happens. The software you use should contain some sort of "password policy" that can be saved along with the website and user name, which ensures that it will generate only legal passwords.

Problem: All this trust in some single piece of software. If I don't have it with me, I'm totally boned, right?

Solution: Ideally, would be a web tool as well as a mobile app, so that there's almost no situation in which you DON'T have it with you. But you are right in principle, of course.

Question: This is a python script, not a mobile app, not a javascript tool.

Answer: That's not a question! But yes, this is merely a proof-of-concept.

