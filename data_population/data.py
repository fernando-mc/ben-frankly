#!/usr/bin/python3

# Loads data into DynamoDB
import boto3
import time

dynamodb_client = boto3.client('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')

table = dynamodb_resource.Table('ben-frankly-dev')

QUOTES = [
    ["He had an excellent constitution of body, was of middle stature, but well set, and very strong; he was ingenious, could draw prettily, was skilled a little in music, and had a clear, pleasing voice"],
    ["he was never employed, the numerous family he had to educate and the straitness of his circumstances keeping him close to his trade; but I remember well his being frequently visited by leading people"],
    ["he was also much consulted by private persons about their affairs when any difficulty occurred, and frequently chosen an arbitrator between contending parties "],
    ["though he was otherwise not an ill-natur'd man: perhaps I was too saucy and provoking."],
    ["a drunken Dutchman"],
    ["I reached through the water to his shock pate, and drew him up, so that we got him in again. His ducking sobered him a little, and he went to sleep"],
    ["She was very hospitable, gave me a dinner of ox-cheek with great good will, accepting only of a pot of ale in return; and I thought myself fixed till Tuesday should come."],
    ["whom he had never seen before, to be one of the town's people that he was the other printer's father"],
    ["an ingenious young man, of excellent character, much respected in the town . . . and a pretty poet."],
    ["appear'd a young man of promising parts"],
    ["he said I had insulted him in such a manner before his people that he could never forget or forgive it. In this, however, he was mistaken."],
    ["he must be of small discretion to think of setting a boy up in business who wanted yet three years of being at man's estate."],
    ["I thank'd her for her kind advice, and promis'd to follow it."],
    ["I waited upon him accordingly, and should have taken Collins with me but that he was not sober."],
    ["[he] treated me with great civility, show'd me his library, which was a very large one, and we had a good deal of conversation about books and authors."],
    ["he met with no success in any application, and continu'd lodging and boarding at the same house with me, and at my expense. "],
    ["Knowing I had that money of Vernon's, he was continually borrowing of me, still promising repayment as soon as he should be in business. "],
    ["His drinking continu'd, about which we sometimes quarrel'd; for, when a little intoxicated, he was very fractious. "],
    ["Once, in a boat on the Delaware with some other young men, he refused to row in his turn. \"I will be row'd home,\" says he. \"We will not row you,\" says I. "],
    ["he came up and struck at me, I clapped my hand under his crutch, and, rising, pitched him head-foremost into the river. I knew he was a good swimmer, and so was under little concern about him; but before he could get round to lay hold of the boat, we had with a few strokes pull'd her out of his reach;"],
    ["he suppos'd me too young to manage business of importance."],
    ["he was too prudent. "],
    ["There was great difference in persons; and discretion did not always accompany years, nor was youth always without it."],
    ["I afterwards heard it as his known character to be liberal of promises which he never meant to keep. "],
    ["I believ'd him one of the best men in the world."],
    ["Osborne dissuaded him, assur'd him he had no genius for poetry, and advis'd him to think of nothing beyond the business he was bred to; "],
    ["he was no better a critic than poet"],
    ["He had brought no money with him, the whole he could muster having been expended in paying his passage. "],
    ["he borrowed occasionally of me to subsist, while he was looking out for business."],
    ["He first endeavoured to get into the play-house, believing himself qualify'd for an actor"],
    ["he changed his name, and did me the honour to assume mine; for I soon after had a letter from him, acquainting me that he was settled in a small village (in Berkshire, I think it was, where he taught reading and writing to ten or a dozen boys, at sixpence each per week)"],
    ["He continued to write frequently, sending me large specimens of an epic poem which he was then composing, and desiring my remarks and corrections. These I gave him from time to time, but endeavour'd rather to discourage his proceeding."],
    ["in the loss of his friendship I found myself relieved from a burthen."],
    ["She was a widow, an elderly woman; had been bred a Protestant, being a clergyman's daughter, but was converted to the Catholic religion by her husband, whose memory she much revered"],
    ["[he] knew a thousand anecdotes of them as far back as the times of Charles the Second. "],
    ["She was lame in her knees with the gout, and, therefore, seldom stirred out of her room, so sometimes wanted company; and hers was so highly amusing to me, that I was sure to spend an evening with her whenever"],
    ["my landlady gave me this account: that she was a Roman Catholic, had been sent abroad when young, and lodg'd in a nunnery with an intent of becoming a nun; but, the country not agreeing with her, she returned to England"],
    ["I was permitted once to visit her. She was cheerful and polite, and convers'd pleasantly. "],
    ["she was never happy, and soon parted from him, refusing to cohabit with him or bear his name, it being now said that he had another wife. "],
    ["He was a worthless fellow, tho' an excellent workman"],
    ["It was an odd thing to find an Oxford scholar in the situation of a bought servant."],
    ["He was not more than eighteen years of age, and gave me this account of himself; that he was born in Gloucester, educated at a grammar-school there, had been distinguish'd among the scholars for some apparent superiority in performing his part, when they exhibited plays"],
    ["[he] had written some pieces in prose and verse, which were printed in the Gloucester newspapers; thence he was sent to Oxford; where he continued about a year, but not well satisfi'd, wishing of all things to see London, and become a player. "],
    ["reason my conversation seem'd to be more valu'd. They had me to their houses, introduced me to their friends, and show'd me much civility; while he, tho' the master, was a little neglected. In truth, he was an odd fish; ignorant of common life, fond of rudely opposing receiv'd opinions, slovenly to extream dirtiness, enthusiastic in some points of religion, and a little knavish withal."],
    ["he began for himself, when young, by wheeling clay for brick-makers, learned to write after he was of age, carri'd the chain for surveyors, who taught him surveying, and he had now by his industry, acquir'd a good estate"],
    ["This gentleman, a stranger to me, stopt one day at my door, and asked me if I was the young man who had lately opened a new printing-house."],
    ["he sent me next year two long letters, containing the best account that had been given of that country, the climate, the soil, husbandry, etc., for in those matters he was very judicious."],
    ["he was at last forc'd to sell his printing-house to satisfy his creditors. "],
    ["He went to Barbadoes, and there lived some years in very poor circumstances."],
    ["I could to raise a party in his favour, and we combated for him awhile with some hopes of success. "],
    ["His mother carried on the business till he was grown up, when I assisted him with an assortment of new types, those of his father being in a manner worn out."],
    ["He was at first permitted to preach in some of our churches; but the clergy, taking a dislike to him, soon refus'd him their pulpits, and he was oblig'd to preach in the fields. "],
    ["The multitudes of all sects and denominations that attended his sermons were enormous"],
    ["he was resolute in his first project, rejected my counsel, and I therefore refus'd to contribute."],
    ["but I, who was intimately acquainted with him (being employed in printing his Sermons and Journals, etc.), never had the least suspicion of his integrity, but am to this day decidedly of opinion that he was in all his conduct a perfectly honest man; and methinks my testimony in his favour ought to have the more weight, as we had no religious connection."],
    ["one might have imagined that, when we met, we could hardly avoid cutting throats; but he was so good-natur'd a man that no personal difference between him and me was occasion'd by the contest, and we often din'd together."],
    ["be necessary, the Assembly, tho' very desirous of making their grant to New England effectual, were at a loss how to accomplish it. Mr. Quincy labored hard with the governor to obtain his assent, but he was obstinate."],
    ["he was totally silent all the first day, and at night only said, \"Who would have thought it?\" "],
    ["he was silent again the following day, saying only at last, \"We shall better know how to deal with them another time"],
    ["he was not very expert"],
    ["But between us personally no enmity arose; we were often together; he was a man of letters, had seen much of the world, and was very entertaining and pleasing in conversation. "],
    ["for, tho' Shirley was not a bred soldier, he was sensible and sagacious in himself, and attentive to good advice from others, capable of forming judicious plans, and quick and active in carrying them into execution."],
    ["which prov'd clearly what our captain suspected, that she was loaded too much by the head."]
]

count = 1
for i in QUOTES:
    print i[0]
    response = table.put_item(
        Item={
                'id': str(count),
                'quote': i[0]
            }
        )
    time.sleep(3)
    count += 1