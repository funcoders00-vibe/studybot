from src.database.database import Base, SessionLocal, engine
from src.models.question_model import Question
from src.models.topic_model import Topic
from src.models.user_model import User
from src.settings import settings
from src.utils.password import hash_password

TOPICS = [('Indian Polity','Constitution and governance','TNPSC_GROUP_1'),('Indian History','Ancient to modern India','TNPSC_GROUP_1'),('Geography','Indian and world geography','COMMON'),('Indian Economy','Economic policy and fundamentals','COMMON'),('General Science','Physics, chemistry and biology','COMMON'),('Aptitude','Quantitative aptitude','RRB_NTPC'),('Reasoning','Logical reasoning','RRB_NTPC')]
QUESTIONS_BY_TOPIC = {
    'Indian Polity': [
        ('Which feature expresses the federal character of the Indian Constitution?', 'Parliamentary system', 'Fundamental rights', 'Directive principles', 'Division of powers between Union and States', 'D', 'The Constitution distributes legislative powers between Union and State governments.', 'MEDIUM'),
        ('Who is the constitutional head of the Union executive?', 'Prime Minister', 'President', 'Chief Justice of India', 'Speaker of Lok Sabha', 'B', 'The President is the constitutional head of the Union executive as per Article 53.', 'EASY'),
        ('Which body conducts elections to Parliament and state legislatures?', 'UPSC', 'Finance Commission', 'Election Commission of India', 'NITI Aayog', 'C', 'The Election Commission of India conducts and supervises elections under Article 324.', 'EASY'),
        ('Under which Article can the President declare a Financial Emergency?', 'Article 352', 'Article 356', 'Article 360', 'Article 365', 'C', 'Article 360 empowers the President to proclaim a Financial Emergency if financial stability is threatened.', 'MEDIUM'),
        ('Which Schedule of the Indian Constitution contains the Anti-Defection Law?', '7th Schedule', '8th Schedule', '9th Schedule', '10th Schedule', 'D', 'The 10th Schedule, added by the 52nd Amendment Act in 1985, contains provisions regarding disqualification on ground of defection.', 'HARD'),
        ('Which Fundamental Right cannot be suspended even during a National Emergency?', 'Article 19', 'Article 20 and 21', 'Article 14 and 15', 'Article 32', 'B', 'Articles 20 (protection in respect of conviction) and 21 (right to life and personal liberty) cannot be suspended.', 'HARD'),
    ],
    'Indian History': [
        ('Who was the founder of the Maurya Empire?', 'Ashoka', 'Chandragupta Maurya', 'Bindusara', 'Brihadratha', 'B', 'Chandragupta Maurya founded the Maurya Empire around 322 BCE with the help of Chanakya.', 'EASY'),
        ('The Indus Valley site of Lothal was situated near which river?', 'Ravi', 'Indus', 'Bhogava', 'Ghaggar', 'C', 'Lothal, the ancient port town of Harappan civilization, was situated on the banks of Bhogava river in Gujarat.', 'MEDIUM'),
        ('Which battle marked the establishment of British political supremacy in Bengal?', 'Battle of Plassey', 'Battle of Buxar', 'Battle of Wandiwash', 'First Carnatic War', 'B', 'The Battle of Buxar (1764) decisively established British political authority and granted Diwani rights.', 'MEDIUM'),
        ('Who presided over the 1929 Lahore Session of the Indian National Congress where Poorna Swaraj was declared?', 'Mahatma Gandhi', 'Subhash Chandra Bose', 'Jawaharlal Nehru', 'Sardar Vallabhbhai Patel', 'C', 'Jawaharlal Nehru presided over the historic Lahore session where complete independence was adopted as the goal.', 'HARD'),
        ('The ancient university of Nalanda was founded during the reign of which Gupta emperor?', 'Samudragupta', 'Chandragupta II', 'Kumaragupta I', 'Skandagupta', 'C', 'Kumaragupta I founded Nalanda University in the 5th century CE.', 'HARD'),
    ],
    'Geography': [
        ('Which is the highest peak in the Western Ghats?', 'Anamudi', 'Doddabetta', 'Mullayanagiri', 'Kalsubai', 'A', 'Anamudi in Kerala (2,695 m) is the highest peak in South India and Western Ghats.', 'EASY'),
        ('The standard meridian of India (82°30\' E) passes through which of the following cities?', 'Lucknow', 'Mirzapur', 'Patna', 'Bhopal', 'B', 'The Indian Standard Time (IST) meridian passes through Mirzapur near Prayagraj.', 'MEDIUM'),
        ('Which soil type is most predominant in the Deccan plateau region?', 'Alluvial soil', 'Black soil', 'Laterite soil', 'Red soil', 'B', 'Black soil (Regur), formed by lava weathering, predominates the Deccan trap and is ideal for cotton.', 'EASY'),
        ('Which river is known as the "Dakshin Ganga" (Ganga of the South)?', 'Krishna', 'Godavari', 'Cauvery', 'Mahanadi', 'B', 'Godavari is called Dakshin Ganga owing to its large length and catchment basin.', 'MEDIUM'),
        ('Which channel separates the Andaman Islands from the Nicobar Islands?', '9 Degree Channel', '10 Degree Channel', 'Duncan Passage', 'Palk Strait', 'B', 'The 10 Degree Channel separates the Andaman Group from the Nicobar Group in the Bay of Bengal.', 'HARD'),
    ],
    'Indian Economy': [
        ('Which institution replaced the Planning Commission of India in 2015?', 'Finance Commission', 'NITI Aayog', 'National Development Council', 'Reserve Bank of India', 'B', 'NITI Aayog (National Institution for Transforming India) replaced the Planning Commission on 1 January 2015.', 'EASY'),
        ('What is the primary indicator used by the RBI to target retail inflation?', 'Wholesale Price Index (WPI)', 'Consumer Price Index (CPI-Combined)', 'GDP Deflator', 'Index of Industrial Production (IIP)', 'B', 'The RBI Monetary Policy Framework uses CPI (Combined) as its nominal anchor for inflation targeting.', 'MEDIUM'),
        ('Which sector contributes the largest share to India\'s Gross Value Added (GVA)?', 'Agriculture and Allied', 'Manufacturing', 'Services', 'Mining and Quarrying', 'C', 'The services sector accounts for over 50% of India’s Gross Value Added.', 'EASY'),
        ('What constitutes the "Fiscal Deficit" in the Union Budget?', 'Revenue Receipts minus Revenue Expenditure', 'Total Expenditure minus Total Receipts excluding borrowings', 'Capital Expenditure minus Capital Receipts', 'Primary Deficit plus Interest Payments', 'B', 'Fiscal Deficit is total expenditure minus total non-debt creating receipts (borrowings excluded).', 'HARD'),
        ('Which committee recommended the implementation of the Goods and Services Tax (GST) in India?', 'Kelkar Task Force', 'Narasimham Committee', 'Rangarajan Committee', 'Tendulkar Committee', 'A', 'The Vijay Kelkar Task Force on implementation of FRBM Act in 2004 recommended a comprehensive GST.', 'HARD'),
    ],
    'General Science': [
        ('Which cell organelle is known as the powerhouse of the cell?', 'Ribosome', 'Mitochondria', 'Golgi apparatus', 'Lysosome', 'B', 'Mitochondria generate ATP through cellular respiration and are termed powerhouses.', 'EASY'),
        ('What is the SI unit of electrical resistance?', 'Volt', 'Ampere', 'Ohm', 'Watt', 'C', 'The ohm (symbol: Ω) is the SI unit of electrical resistance.', 'EASY'),
        ('Which gas is primarily responsible for the greenhouse effect on Earth?', 'Methane', 'Carbon dioxide', 'Water vapor', 'Nitrous oxide', 'C', 'Water vapor is the largest contributor to the natural greenhouse effect, though CO2 is the primary anthropogenic driver.', 'MEDIUM'),
        ('Sound waves cannot travel through which of the following media?', 'Solids', 'Liquids', 'Gases', 'Vacuum', 'D', 'Sound waves are mechanical waves requiring a material medium for propagation.', 'EASY'),
        ('Which enzyme initiates the digestion of starch in the human mouth?', 'Pepsin', 'Salivary Amylase (Ptyalin)', 'Trypsin', 'Lipase', 'B', 'Salivary amylase breaks down complex starch into maltose and dextrin in the mouth.', 'MEDIUM'),
    ],
    'Aptitude': [
        ('A train 150m long is running at 54 km/h. How much time does it take to cross a pole?', '10 seconds', '12 seconds', '15 seconds', '8 seconds', 'A', '54 km/h = 54 * 5/18 = 15 m/s. Time = Distance / Speed = 150 / 15 = 10 seconds.', 'EASY'),
        ('If the cost price of 12 items equals the selling price of 10 items, what is the profit percentage?', '16.67%', '20%', '25%', '15%', 'B', 'Profit % = ((12 - 10) / 10) * 100 = (2 / 10) * 100 = 20%.', 'MEDIUM'),
        ('A and B together can complete a work in 12 days. A alone can do it in 20 days. In how many days can B alone complete it?', '25 days', '30 days', '36 days', '28 days', 'B', '1/B = 1/12 - 1/20 = (5 - 3)/60 = 2/60 = 1/30. B completes it in 30 days.', 'MEDIUM'),
        ('What is the compound interest on Rs. 10,000 at 10% per annum for 2 years compounded annually?', 'Rs. 2,000', 'Rs. 2,100', 'Rs. 2,200', 'Rs. 2,050', 'B', 'Amount = 10000 * (1.1)^2 = 12,100. CI = 12,100 - 10,000 = 2,100.', 'MEDIUM'),
        ('The average of 5 consecutive odd numbers is 27. What is the largest of these numbers?', '29', '31', '33', '35', 'B', 'For consecutive odd numbers, the average is the middle number (3rd). So numbers are 23, 25, 27, 29, 31. Largest is 31.', 'HARD'),
    ],
    'Reasoning': [
        ('Look at this series: 7, 10, 8, 11, 9, 12, ... What number should come next?', '10', '12', '13', '14', 'A', 'Alternating addition and subtraction: +3, -2, +3, -2, +3, -2. Next is 12 - 2 = 10.', 'EASY'),
        ('If "ROSE" is coded as 6821 and "CHAIR" is coded as 73456, what is the code for "SEARCH"?', '214673', '214763', '216473', '241673', 'A', 'Direct letter coding: S=2, E=1, A=4, R=6, C=7, H=3 => 214673.', 'MEDIUM'),
        ('Pointing to a photograph, a man said: "I have no brother or sister, but that man\'s father is my father\'s son." Whose photograph was it?', 'His father\'s', 'His son\'s', 'His own', 'His nephew\'s', 'B', '"My father\'s son" is the man himself (no siblings). So the photograph\'s father is the speaker, making it his son\'s photograph.', 'MEDIUM'),
        ('Statement: All mangoes are fruits. All fruits are sweet. Conclusion I: All mangoes are sweet. Conclusion II: Some sweet things are mangoes.', 'Only I follows', 'Only II follows', 'Neither I nor II follows', 'Both I and II follow', 'D', 'Since all mangoes are in fruits and all fruits are in sweet, mangoes are sweet (I) and the intersection of sweet and mangoes exists (II). Both follow.', 'HARD'),
        ('In a certain code, "CLOCK" is written as "CNSMS". How is "WATCH" written in that code?', 'WBVDJ', 'WCVDJ', 'XCUCI', 'XBVDJ', 'B', 'Pattern: +0, +1, +2, +1, +0: W+0=W, A+1=B, T+2=V, C+1=D, H+0=H => or W(+0)=W, A(+2)=C, T(+2)=V, C(+1)=D, H(+2)=J. W(+0)=W, A(+2)=C, T(+2)=V, C(+1)=D, H(+2)=J => WCVDJ.', 'HARD'),
    ]
}

def seed():
    Base.metadata.create_all(bind=engine)
    if not settings.tamil_password: raise RuntimeError('Set TAMIL_PASSWORD in .env before running the seeder.')
    db = SessionLocal()
    try:
        if not db.query(User).filter_by(email=settings.tamil_email).first():
            db.add(User(name='Tamil', email=settings.tamil_email, password_hash=hash_password(settings.tamil_password)))
        db.flush()
        for name, description, category in TOPICS:
            if not db.query(Topic).filter_by(name=name).first():
                db.add(Topic(name=name, description=description, exam_category=category))
        db.flush()

        # Seed questions across topics
        for topic_name, questions in QUESTIONS_BY_TOPIC.items():
            topic_record = db.query(Topic).filter_by(name=topic_name).first()
            if not topic_record:
                continue
            for q, a, b, c, d, correct, explanation, diff in questions:
                exists = db.query(Question).filter_by(topic_id=topic_record.id, question_text=q).first()
                if not exists:
                    db.add(Question(
                        topic_id=topic_record.id,
                        question_text=q,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_option=correct,
                        explanation=explanation,
                        difficulty=diff,
                        source_book='Standard Question Bank',
                        source_chapter=topic_name,
                        source_page='1'
                    ))
        db.commit()
    finally:
        db.close()

if __name__ == '__main__': seed()

