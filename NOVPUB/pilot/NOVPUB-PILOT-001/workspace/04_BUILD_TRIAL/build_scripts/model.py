import json,re
TITLE="The Blue Silence"; AUTHOR="Darya Malak"; YEAR="2026"
COPY_LINES=[
 "Copyright © 2026 Darya Malak. All rights reserved.",
 "No part of this book may be reproduced, stored in a retrieval system, or transmitted in any form or by any means without the prior written permission of the copyright holder, except for brief quotations in a review.",
 "This is a work of fiction. Names, characters, organisations, places, events and incidents are either the product of the author’s imagination or used fictitiously. Any resemblance to actual persons, living or dead, or to actual organisations or events, is purely coincidental.",
 "First edition, 2026.",
 "ISBN (paperback): [to be assigned]",
 "ISBN (ebook): [to be assigned]",
 "Published by Darya Malak.",
]
TRIAL="TRIAL BUILD — NOT FOR SALE OR DISTRIBUTION"
def load():
    ch=json.load(open('chapters.json')); out=[]
    for c in ch:
        it=c['items']; b=[]; head=None
        n=[x for x in it if x['style']=='Heading 1'][0]['text']
        t=[x for x in it if x['style']=='Heading 2'][0]['text']
        loc=it[2]['text']; assert it[2]['ital'] and it[2]['center']
        body=it[3:]
        # drop END CHAPTER X and the trailing scene break before it
        while body and re.match(r'END CHAPTER',body[-1]['text']): body.pop()
        if body and body[-1]['style']=='Scene Break' and len(body)<len(it)-3: body.pop()
        for x in body:
            if x['style']=='Scene Break': b.append(('scene',''))
            elif x['text']=='END OF BOOK ONE': b.append(('end',x['text']))
            elif x['center'] and x['bold']: b.append(('insert',x['text']))
            else: b.append(('p',x['text']))
        # collapse scene break at very end of chapter
        while b and b[-1][0]=='scene': b.pop()
        out.append(dict(num=n,title=t,loc=loc,blocks=b))
    return out
def title_case(s): return s.title().replace("’S","’s").replace("'S","’s")
if __name__=='__main__':
    L=load(); print(len(L),L[0]['num'],L[0]['title'],L[1]['num'],L[-1]['blocks'][-3:])
    import collections
    print(collections.Counter(k for c in L for k,_ in c['blocks']))
