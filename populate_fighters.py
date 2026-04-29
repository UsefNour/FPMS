#!/usr/bin/env python3
"""
Script to populate the FPMS database with MMA fighters.
Run this script to add a comprehensive list of MMA fighters to your database.
"""

from app import app, db
from models import Fighter

def populate_fighters():
    """Populate the database with professional MMA fighters."""

    fighters_data = [
        # Heavyweight Champions
        {
            "name": "Jon Jones",
            "nickname": "Bones",
            "weight_class": "Light Heavyweight",
            "record": "27-1-0",
            "fighting_style": "Striking, Wrestling",
            "strengths": "Striking, Wrestling, Cardio, Footwork",
            "weaknesses": "Occasional recklessness, Chin durability",
            "notable_fights": "Defeated Daniel Cormier (UFC 214), Dominated Alexander Gustafsson (UFC 165), Beat Rashad Evans (UFC 145)"
        },
        {
            "name": "Francis Ngannou",
            "nickname": "The Predator",
            "weight_class": "Heavyweight",
            "record": "17-3-0",
            "fighting_style": "Boxing, Kickboxing",
            "strengths": "Power punching, Knockout power, Athleticism",
            "weaknesses": "Ground game, Wrestling defense",
            "notable_fights": "KO'd Alistair Overeem (UFC 218), Beat Cain Velasquez (UFC 260), Lost to Stipe Miocic (UFC 260)"
        },
        {
            "name": "Stipe Miocic",
            "nickname": "",
            "weight_class": "Heavyweight",
            "record": "20-4-0",
            "fighting_style": "Boxing, Wrestling",
            "strengths": "Boxing, Wrestling, Cardio, Chin",
            "weaknesses": "Occasional slow starts, Power punching",
            "notable_fights": "Defeated Francis Ngannou (UFC 260), Beat Daniel Cormier (UFC 226), Lost to Jon Jones (UFC 197)"
        },
        {
            "name": "Ciryl Gane",
            "nickname": "Bon Gamin",
            "weight_class": "Heavyweight",
            "record": "12-2-0",
            "fighting_style": "Kickboxing, Wrestling",
            "strengths": "Striking, Wrestling, Cardio",
            "weaknesses": "Ground game, Submissions",
            "notable_fights": "Defeated Derrick Lewis (UFC 270), Beat Alexander Volkov (UFC 256), Lost to Francis Ngannou (UFC 270)"
        },
        {
            "name": "Derrick Lewis",
            "nickname": "The Black Beast",
            "weight_class": "Heavyweight",
            "record": "28-11-0",
            "fighting_style": "Boxing, Kickboxing",
            "strengths": "Power punching, Knockout power, Athleticism",
            "weaknesses": "Ground game, Wrestling defense",
            "notable_fights": "KO'd Junior dos Santos (UFC 226), Beat Curtis Blaydes (UFC 265), Lost to Ciryl Gane (UFC 270)"
        },
        {
            "name": "Curtis Blaydes",
            "nickname": "",
            "weight_class": "Heavyweight",
            "record": "17-4-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Takedowns, Ground control",
            "weaknesses": "Striking defense, Cardio",
            "notable_fights": "Defeated Derrick Lewis (UFC 265), Beat Francis Ngannou (UFC 246), Lost to Jon Jones (UFC 235)"
        },

        # Light Heavyweight
        {
            "name": "Alex Pereira",
            "nickname": "Poatan",
            "weight_class": "Light Heavyweight",
            "record": "9-2-0",
            "fighting_style": "Kickboxing, Muay Thai",
            "strengths": "Striking, Knockout power, Kicks",
            "weaknesses": "Ground game, Wrestling",
            "notable_fights": "KO'd Jan Blachowicz (UFC 295), Beat Israel Adesanya (UFC 281), Lost to Jamahal Hill (UFC 300)"
        },
        {
            "name": "Jamahal Hill",
            "nickname": "Sweet Dreams",
            "weight_class": "Light Heavyweight",
            "record": "12-2-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Takedowns, Ground control",
            "weaknesses": "Striking defense, Cardio",
            "notable_fights": "Defeated Alex Pereira (UFC 300), Beat Thiago Santos (UFC 283), Lost to Glover Teixeira (UFC 283)"
        },
        {
            "name": "Glover Teixeira",
            "nickname": "",
            "weight_class": "Light Heavyweight",
            "record": "34-8-0",
            "fighting_style": "Brazilian Jiu-Jitsu, Wrestling",
            "strengths": "Brazilian Jiu-Jitsu, Submissions, Ground control",
            "weaknesses": "Striking, Cardio",
            "notable_fights": "Defeated Jamahal Hill (UFC 283), Beat Anthony Smith (UFC 272), Lost to Jon Jones (UFC 172)"
        },
        {
            "name": "Anthony Smith",
            "nickname": "Lionheart",
            "weight_class": "Light Heavyweight",
            "record": "38-19-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Takedowns, Cardio",
            "weaknesses": "Striking power, Knockout vulnerability",
            "notable_fights": "Defeated Glover Teixeira (UFC 272), Beat Volkan Oezdemir (UFC 241), Lost to Glover Teixeira (UFC 283)"
        },
        {
            "name": "Volkan Oezdemir",
            "nickname": "No Time",
            "weight_class": "Light Heavyweight",
            "record": "19-7-0",
            "fighting_style": "Kickboxing, Wrestling",
            "strengths": "Striking, Knockout power, Kicks",
            "weaknesses": "Ground game, Wrestling defense",
            "notable_fights": "Defeated Anthony Smith (UFC 241), Beat Jimi Manuwa (UFC 221), Lost to Anthony Smith (UFC 272)"
        },

        # Middleweight
        {
            "name": "Sean Strickland",
            "nickname": "Tarzan",
            "weight_class": "Middleweight",
            "record": "28-6-0",
            "fighting_style": "Boxing, Wrestling",
            "strengths": "Boxing, Wrestling, Cardio, Pressure",
            "weaknesses": "Occasional reckless aggression",
            "notable_fights": "Defeated Jared Cannonier (UFC 297), Beat Paulo Costa (UFC 293), Lost to Israel Adesanya (UFC 293)"
        },
        {
            "name": "Marvin Vettori",
            "nickname": "The Italian Stallion",
            "weight_class": "Middleweight",
            "record": "19-6-1",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Takedowns, Ground control",
            "weaknesses": "Striking defense, Cardio",
            "notable_fights": "Defeated Paulo Costa (UFC 264), Beat Jack Hermansson (UFC 262), Lost to Sean Strickland (UFC 297)"
        },
        {
            "name": "Paulo Costa",
            "nickname": "The Eraser",
            "weight_class": "Middleweight",
            "record": "14-3-0",
            "fighting_style": "Brazilian Jiu-Jitsu, Wrestling",
            "strengths": "Brazilian Jiu-Jitsu, Submissions, Ground control",
            "weaknesses": "Striking, Cardio",
            "notable_fights": "Defeated Marvin Vettori (UFC 264), Beat Yoel Romero (UFC 258), Lost to Sean Strickland (UFC 293)"
        },
        {
            "name": "Jared Cannonier",
            "nickname": "The Killa Gorilla",
            "weight_class": "Middleweight",
            "record": "17-6-0",
            "fighting_style": "Boxing, Wrestling",
            "strengths": "Boxing, Wrestling, Cardio, Pressure",
            "weaknesses": "Occasional reckless aggression",
            "notable_fights": "Defeated Sean Strickland (UFC 297), Beat Derek Brunson (UFC 289), Lost to Sean Strickland (UFC 297)"
        },
        {
            "name": "Derek Brunson",
            "nickname": "The One-Man Army",
            "weight_class": "Middleweight",
            "record": "23-9-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Takedowns, Ground control",
            "weaknesses": "Striking defense, Cardio",
            "notable_fights": "Defeated Jared Cannonier (UFC 289), Beat Elias Theodorou (UFC 280), Lost to Jared Cannonier (UFC 289)"
        },

        # Welterweight
        {
            "name": "Kamaru Usman",
            "nickname": "The Nigerian Nightmare",
            "weight_class": "Welterweight",
            "record": "20-4-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Takedowns, Ground control, Cardio",
            "weaknesses": "Striking power, Knockout vulnerability",
            "notable_fights": "Defeated Leon Edwards (UFC 278), Beat Jorge Masvidal (UFC 261), Lost to Colby Covington (UFC 245)"
        },
        {
            "name": "Leon Edwards",
            "nickname": "Rocky",
            "weight_class": "Welterweight",
            "record": "22-4-0",
            "fighting_style": "Striking, Boxing",
            "strengths": "Striking, Footwork, Cardio, Defense",
            "weaknesses": "Takedowns, Ground game",
            "notable_fights": "Defeated Kamaru Usman (UFC 278), Beat Nate Diaz (UFC 269), Lost to Kamaru Usman (UFC 278)"
        },
        {
            "name": "Vicente Luque",
            "nickname": "",
            "weight_class": "Welterweight",
            "record": "22-9-1",
            "fighting_style": "Brazilian Jiu-Jitsu, Wrestling",
            "strengths": "Brazilian Jiu-Jitsu, Submissions, Ground control",
            "weaknesses": "Striking, Cardio",
            "notable_fights": "Defeated Geoff Neal (UFC 294), Beat Michael Chiesa (UFC 265), Lost to Leon Edwards (UFC 278)"
        },
        {
            "name": "Geoff Neal",
            "nickname": "Handz of Steel",
            "weight_class": "Welterweight",
            "record": "15-5-0",
            "fighting_style": "Boxing, Wrestling",
            "strengths": "Boxing, Wrestling, Cardio, Pressure",
            "weaknesses": "Occasional reckless aggression",
            "notable_fights": "Defeated Vicente Luque (UFC 294), Beat Santiago Ponzinibbio (UFC 294), Lost to Vicente Luque (UFC 294)"
        },
        {
            "name": "Rafael Fiziev",
            "nickname": "Ataman",
            "weight_class": "Welterweight",
            "record": "12-3-0",
            "fighting_style": "Wrestling, Sambo",
            "strengths": "Wrestling, Takedowns, Ground control, Cardio",
            "weaknesses": "Occasional striking exchanges",
            "notable_fights": "Defeated Islam Makhachev (UFC 279), Beat Renato Moicano (UFC 279), Lost to Leon Edwards (UFC 278)"
        },

        # Lightweight
        {
            "name": "Islam Makhachev",
            "nickname": "",
            "weight_class": "Lightweight",
            "record": "25-1-0",
            "fighting_style": "Wrestling, Sambo",
            "strengths": "Wrestling, Takedowns, Ground control, Cardio",
            "weaknesses": "Occasional striking exchanges",
            "notable_fights": "Defeated Alexander Volkanovski (UFC 294), Beat Bobby Green (UFC 291), Lost to Rafael Fiziev (UFC 279)"
        },
        {
            "name": "Charles Oliveira",
            "nickname": "Do Bronx",
            "weight_class": "Lightweight",
            "record": "34-10-0",
            "fighting_style": "Brazilian Jiu-Jitsu",
            "strengths": "Brazilian Jiu-Jitsu, Submissions, Guard play",
            "weaknesses": "Striking, Cardio",
            "notable_fights": "Defeated Islam Makhachev (UFC 280), Beat Michael Chandler (UFC 262), Lost to Tony Ferguson (UFC 256)"
        },
        {
            "name": "Conor McGregor",
            "nickname": "The Notorious",
            "weight_class": "Lightweight",
            "record": "22-6-0",
            "fighting_style": "Boxing, Kickboxing",
            "strengths": "Striking, Knockout power, Athleticism",
            "weaknesses": "Ground game, Wrestling defense",
            "notable_fights": "Defeated Dustin Poirier (UFC 264), Beat Donald Cerrone (UFC 246), Lost to Khabib Nurmagomedov (UFC 229)"
        },
        {
            "name": "Dustin Poirier",
            "nickname": "The Diamond",
            "weight_class": "Lightweight",
            "record": "29-8-0",
            "fighting_style": "Boxing, Wrestling",
            "strengths": "Boxing, Wrestling, Cardio, Pressure",
            "weaknesses": "Occasional reckless aggression",
            "notable_fights": "Defeated Conor McGregor (UFC 264), Beat Max Holloway (UFC 264), Lost to Conor McGregor (UFC 264)"
        },
        {
            "name": "Justin Gaethje",
            "nickname": "The Highlight",
            "weight_class": "Lightweight",
            "record": "25-4-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Takedowns, Ground control",
            "weaknesses": "Striking defense, Cardio",
            "notable_fights": "Defeated Khabib Nurmagomedov (UFC 254), Beat Tony Ferguson (UFC 249), Lost to Charles Oliveira (UFC 274)"
        },

        # Featherweight
        {
            "name": "Alexander Volkanovski",
            "nickname": "The Great",
            "weight_class": "Featherweight",
            "record": "26-4-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Striking, Cardio, Versatility",
            "weaknesses": "Occasional overconfidence",
            "notable_fights": "Defeated Islam Makhachev (UFC 294), Beat Max Holloway (UFC 245), Lost to Jose Aldo (UFC 237)"
        },
        {
            "name": "Ilia Topuria",
            "nickname": "",
            "weight_class": "Featherweight",
            "record": "15-0-0",
            "fighting_style": "Striking, Wrestling",
            "strengths": "Striking, Wrestling, Cardio, Youth",
            "weaknesses": "Limited experience, Unproven at highest level",
            "notable_fights": "Defeated Max Holloway (UFC 298), Beat Bryce Mitchell (UFC 298), Beat Jai Herbert (UFC 298)"
        },
        {
            "name": "Max Holloway",
            "nickname": "Blessed",
            "weight_class": "Featherweight",
            "record": "25-7-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Striking, Cardio, Versatility",
            "weaknesses": "Occasional overconfidence",
            "notable_fights": "Defeated Alexander Volkanovski (UFC 245), Beat Jose Aldo (UFC 212), Lost to Ilia Topuria (UFC 298)"
        },
        {
            "name": "Yair Rodriguez",
            "nickname": "Pantera",
            "weight_class": "Featherweight",
            "record": "16-4-1",
            "fighting_style": "Kickboxing, Wrestling",
            "strengths": "Striking, Knockout power, Kicks",
            "weaknesses": "Ground game, Wrestling defense",
            "notable_fights": "Defeated Brian Ortega (UFC 284), Beat Calvin Kattar (UFC 284), Lost to Alexander Volkanovski (UFC 294)"
        },
        {
            "name": "Brian Ortega",
            "nickname": "T-City",
            "weight_class": "Featherweight",
            "record": "16-3-0",
            "fighting_style": "Brazilian Jiu-Jitsu, Wrestling",
            "strengths": "Brazilian Jiu-Jitsu, Submissions, Guard play",
            "weaknesses": "Striking, Cardio",
            "notable_fights": "Defeated Yair Rodriguez (UFC 284), Beat Chan Sung Jung (UFC 250), Lost to Yair Rodriguez (UFC 284)"
        },

        # Bantamweight
        {
            "name": "Sean O'Malley",
            "nickname": "Suga",
            "weight_class": "Bantamweight",
            "record": "17-1-0",
            "fighting_style": "Boxing, Muay Thai",
            "strengths": "Striking, Footwork, Knockout power",
            "weaknesses": "Ground game, Wrestling defense",
            "notable_fights": "Defeated Marlon Vera (UFC 299), Beat Merab Dvalishvili (UFC 299), Lost to Marlon Vera (UFC 287)"
        },
        {
            "name": "Marlon Vera",
            "nickname": "Chito",
            "weight_class": "Bantamweight",
            "record": "21-9-1",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Cardio, Pressure fighting",
            "weaknesses": "Striking power, Knockout vulnerability",
            "notable_fights": "Defeated Sean O'Malley (UFC 287), Beat Dominick Cruz (UFC 269), Lost to Sean O'Malley (UFC 299)"
        },
        {
            "name": "Merab Dvalishvili",
            "nickname": "The Machine",
            "weight_class": "Bantamweight",
            "record": "16-4-0",
            "fighting_style": "Wrestling, Sambo",
            "strengths": "Wrestling, Takedowns, Ground control, Cardio",
            "weaknesses": "Occasional striking exchanges",
            "notable_fights": "Defeated Sean O'Malley (UFC 299), Beat Petr Yan (UFC 299), Lost to Sean O'Malley (UFC 299)"
        },
        {
            "name": "Petr Yan",
            "nickname": "No Mercy",
            "weight_class": "Bantamweight",
            "record": "17-5-0",
            "fighting_style": "Boxing, Wrestling",
            "strengths": "Boxing, Wrestling, Cardio, Pressure",
            "weaknesses": "Occasional reckless aggression",
            "notable_fights": "Defeated Merab Dvalishvili (UFC 299), Beat Jose Aldo (UFC 259), Lost to Merab Dvalishvili (UFC 299)"
        },
        {
            "name": "Dominick Cruz",
            "nickname": "The Dominator",
            "weight_class": "Bantamweight",
            "record": "24-4-0",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Takedowns, Ground control",
            "weaknesses": "Striking defense, Cardio",
            "notable_fights": "Defeated Marlon Vera (UFC 269), Beat Cody Garbrandt (UFC 207), Lost to Marlon Vera (UFC 269)"
        },

        # Flyweight
        {
            "name": "Alexandre Pantoja",
            "nickname": "",
            "weight_class": "Flyweight",
            "record": "29-5-0",
            "fighting_style": "Brazilian Jiu-Jitsu, Wrestling",
            "strengths": "Brazilian Jiu-Jitsu, Wrestling, Submissions",
            "weaknesses": "Striking power, Cardio",
            "notable_fights": "Defeated Brandon Moreno (UFC 301), Beat Askar Askarov (UFC 301), Lost to Brandon Moreno (UFC 290)"
        },
        {
            "name": "Brandon Moreno",
            "nickname": "The Assassin Baby",
            "weight_class": "Flyweight",
            "record": "21-8-2",
            "fighting_style": "Wrestling, Boxing",
            "strengths": "Wrestling, Grappling, Cardio",
            "weaknesses": "Striking power, Knockout vulnerability",
            "notable_fights": "Defeated Alexandre Pantoja (UFC 290), Beat Kai Kara-France (UFC 269), Lost to Alexandre Pantoja (UFC 301)"
        },
        {
            "name": "Kai Kara-France",
            "nickname": "",
            "weight_class": "Flyweight",
            "record": "25-11-0",
            "fighting_style": "Muay Thai, Boxing",
            "strengths": "Striking, Footwork, Knockout power",
            "weaknesses": "Ground game, Wrestling defense",
            "notable_fights": "Defeated Brandon Moreno (UFC 269), Beat Cody Stamann (UFC 269), Lost to Brandon Moreno (UFC 269)"
        },
        {
            "name": "Askar Askarov",
            "nickname": "",
            "weight_class": "Flyweight",
            "record": "16-2-1",
            "fighting_style": "Wrestling, Sambo",
            "strengths": "Wrestling, Takedowns, Ground control, Cardio",
            "weaknesses": "Occasional striking exchanges",
            "notable_fights": "Defeated Alexandre Pantoja (UFC 301), Beat Kai Kara-France (UFC 301), Lost to Alexandre Pantoja (UFC 301)"
        },
        {
            "name": "Cody Stamann",
            "nickname": "",
            "weight_class": "Flyweight",
            "record": "21-6-1",
            "fighting_style": "Brazilian Jiu-Jitsu, Wrestling",
            "strengths": "Brazilian Jiu-Jitsu, Submissions, Guard play",
            "weaknesses": "Striking, Cardio",
            "notable_fights": "Defeated Kai Kara-France (UFC 269), Beat Cortney Casey (UFC 269), Lost to Kai Kara-France (UFC 269)"
        },

        # Women's Divisions
        {
            "name": "Amanda Nunes",
            "nickname": "The Lioness",
            "weight_class": "Featherweight",
            "record": "23-5-0",
            "fighting_style": "Brazilian Jiu-Jitsu, Boxing",
            "strengths": "Brazilian Jiu-Jitsu, Boxing, Versatility",
            "weaknesses": "Occasional overconfidence",
            "notable_fights": "Defeated Julianna Peña (UFC 289), Beat Irene Aldana (UFC 289), Lost to Julianna Peña (UFC 277)"
        },
        {
            "name": "Zhang Weili",
            "nickname": "",
            "weight_class": "Strawweight",
            "record": "25-3-0",
            "fighting_style": "Sanda, Wrestling",
            "strengths": "Striking, Wrestling, Cardio",
            "weaknesses": "Ground game, Submissions",
            "notable_fights": "Defeated Rose Namajunas (UFC 268), Beat Joanna Jedrzejczyk (UFC 248), Lost to Rose Namajunas (UFC 261)"
        }
    ]

    with app.app_context():
        # Clear existing fighters
        Fighter.query.delete()
        db.session.commit()

        # Add new fighters
        for fighter_data in fighters_data:
            fighter = Fighter(**fighter_data)
            db.session.add(fighter)

        db.session.commit()
        print(f"Successfully added {len(fighters_data)} fighters to the database!")

if __name__ == "__main__":
    populate_fighters()
