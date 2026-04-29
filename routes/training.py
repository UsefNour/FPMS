from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, FighterProfile, CampPlan, GamePlan, WeightLog, Fighter
from forms import FighterProfileForm, CampPlanForm, GamePlanForm, WeightLogForm
from datetime import datetime
import os
import json

training_bp = Blueprint('training', __name__)


def generate_camp_plan(strengths, weaknesses, weeks_remaining, fight_type):
    strengths_lower = strengths.lower()
    weaknesses_lower = weaknesses.lower()

    striking_keywords = ['striking', 'punching', 'boxing', 'kickboxing', 'muay thai', 'karate', 'knockout', 'ko', 'hands', 'kicks']
    wrestling_keywords = ['wrestling', 'takedowns', 'takedown', 'control', 'cage control', 'clinch', 'dirty boxing']
    bjj_keywords = ['bjj', 'jiu-jitsu', 'jujitsu', 'submissions', 'submission', 'guard', 'ground game', 'chokes']
    grappling_keywords = wrestling_keywords + bjj_keywords + ['grappling', 'ground', 'gnp']
    cardio_keywords = ['cardio', 'conditioning', 'endurance', 'pace', 'volume', 'gas tank', 'stamina']
    power_keywords = ['power', 'knockout', 'ko', 'heavy hands', 'dangerous', 'finisher']
    pressure_keywords = ['pressure', 'aggression', 'aggressive', 'forward', 'relentless']
    speed_keywords = ['speed', 'fast', 'quick', 'explosive', 'athletic']

    opp_striking = any(kw in strengths_lower for kw in striking_keywords)
    opp_wrestling = any(kw in strengths_lower for kw in wrestling_keywords)
    opp_grappling = any(kw in strengths_lower for kw in grappling_keywords)
    opp_cardio = any(kw in strengths_lower for kw in cardio_keywords)
    opp_power = any(kw in strengths_lower for kw in power_keywords)
    opp_pressure = any(kw in strengths_lower for kw in pressure_keywords)
    opp_speed = any(kw in strengths_lower for kw in speed_keywords)

    weak_striking = any(kw in weaknesses_lower for kw in striking_keywords)
    weak_grappling = any(kw in weaknesses_lower for kw in grappling_keywords)
    weak_wrestling = any(kw in weaknesses_lower for kw in wrestling_keywords)
    weak_cardio = any(kw in weaknesses_lower for kw in cardio_keywords)
    weak_tdd = any(kw in weaknesses_lower for kw in ['tdd', 'takedown defense', 'gets taken down'])
    weak_chin = any(kw in weaknesses_lower for kw in ['chin', 'durability', 'gets hurt'])
    weak_defense = any(kw in weaknesses_lower for kw in ['defense', 'defensive', 'guard'])

    training_priorities = []
    sparring_focus = []
    technique_drills = []
    conditioning_focus = []
    mental_prep = []

    if opp_striking:
        training_priorities.append("Defensive boxing and head movement")
        sparring_focus.append("Stand-up defense with skilled strikers")
        technique_drills.append("Slipping, parrying, and check hooks")
        mental_prep.append("Stay calm under fire, don't panic when hit")

    if opp_wrestling:
        training_priorities.append("Takedown defense and cage work")
        sparring_focus.append("Wrestling-heavy rounds against strong wrestlers")
        technique_drills.append("Sprawls, underhooks, whizzers, cage wrestling")
        mental_prep.append("Maintain composure when pressed against cage")

    if opp_grappling:
        training_priorities.append("Submission defense and escapes")
        sparring_focus.append("Positional sparring starting in bad positions")
        technique_drills.append("Guard retention, submission defense, stand-ups")
        mental_prep.append("Stay patient on bottom, look for opportunities")

    if opp_cardio:
        conditioning_focus.append("Match or exceed opponent's pace - 5+ rounds of hard sparring")
        training_priorities.append("High-volume conditioning work")
        mental_prep.append("Prepare for a grueling fight - no easy rounds")

    if opp_power:
        training_priorities.append("Chin tucked, hands up at ALL times")
        sparring_focus.append("Defensive sparring with power punchers")
        technique_drills.append("Defensive footwork and distance management")
        mental_prep.append("Respect power but don't fear it")

    if opp_pressure:
        training_priorities.append("Circle and angle work to avoid cage")
        conditioning_focus.append("Pace work - moving while throwing")
        technique_drills.append("Pivots, lateral movement, jab and move")
        mental_prep.append("Don't let pressure make you panic")

    if opp_speed:
        training_priorities.append("Timing and anticipation drills")
        sparring_focus.append("Fast-paced sparring with quick opponents")
        technique_drills.append("Reading feints, timing counters")

    if weak_striking:
        training_priorities.append("Sharpen striking combinations for openings")
        sparring_focus.append("Aggressive offensive striking rounds")
        technique_drills.append("Power combinations, setups, and finishes")

    if weak_grappling or weak_wrestling or weak_tdd:
        training_priorities.append("Wrestling offense and top control")
        sparring_focus.append("Takedown hunting and ground control")
        technique_drills.append("Chain wrestling, ground and pound combos")

    if weak_cardio:
        conditioning_focus.append("Push pace to break opponent - volume training")
        training_priorities.append("Build cardio advantage for late rounds")
        mental_prep.append("Be ready to pour it on when they fade")

    if weak_chin:
        training_priorities.append("Power shot setups and finishing combos")
        sparring_focus.append("Working on timing power shots after combos")
        technique_drills.append("Lead hooks, overhand rights, body-head combos")

    if weak_defense:
        training_priorities.append("Volume striking and pressure")
        technique_drills.append("Long combinations, feint-attack patterns")

    if not training_priorities:
        training_priorities = ["General MMA preparation", "Well-rounded skill development"]
    if not sparring_focus:
        sparring_focus = ["Full MMA sparring with variety of styles"]
    if not technique_drills:
        technique_drills = ["Fundamental techniques across all ranges"]
    if not conditioning_focus:
        conditioning_focus = ["Standard fight camp conditioning protocol"]
    if not mental_prep:
        mental_prep = ["Visualization and mental rehearsal"]

    is_five_rounds = '5' in fight_type
    phases = {}

    if weeks_remaining >= 10:
        phases = {
            "Phase 1 - Foundation": {
                "duration": "Weeks 1-3",
                "focus": f"Build base while addressing opponent's strengths",
                "training_priorities": training_priorities[:2] if len(training_priorities) > 2 else training_priorities,
                "conditioning": "Build aerobic base: 3-4 cardio sessions, 3 strength sessions",
                "sparring": "Technical sparring only - 2 sessions/week",
                "techniques": technique_drills[:3],
                "recovery": "Full recovery protocols, 8+ hours sleep",
                "mental": "Begin visualizing the fight and opponent tendencies"
            },
            "Phase 2 - Build": {
                "duration": "Weeks 4-5",
                "focus": f"Increase intensity while drilling specific techniques",
                "training_priorities": training_priorities,
                "conditioning": conditioning_focus[0] if conditioning_focus else "Increase cardio intensity",
                "sparring": sparring_focus[:2],
                "techniques": technique_drills,
                "recovery": "Active recovery, mobility work, massage",
                "mental": mental_prep[:1] if mental_prep else ["Build confidence"]
            },
            "Phase 3 - Skill Sharpening": {
                "duration": "Weeks 6-7",
                "focus": "Perfect fight-specific skills for this opponent",
                "training_priorities": training_priorities,
                "conditioning": f"Fight simulation: {5 if is_five_rounds else 3} hard rounds + 1 overtime",
                "sparring": sparring_focus,
                "techniques": technique_drills,
                "recovery": "Prioritize recovery between hard sessions",
                "mental": mental_prep
            },
            "Phase 4 - Peak Sparring": {
                "duration": "Weeks 8-9",
                "focus": "Full fight simulation with opponent-style partners",
                "training_priorities": training_priorities[:2],
                "conditioning": "Maintain - don't overtrain",
                "sparring": ["Full fight simulations against opponent-style partners", "4-5 hard sparring sessions/week"],
                "techniques": ["Sharpen finishing sequences", "Review counters to opponent's best weapons"],
                "recovery": "Ice baths, compression, enhanced sleep",
                "mental": ["Fight visualization daily", "Review opponent footage"]
            },
            "Phase 5 - Taper": {
                "duration": "Final Week",
                "focus": "Peak performance - reduce volume, maintain intensity",
                "training_priorities": ["Light technique review", "Stay sharp without overtraining"],
                "conditioning": "Light movement, mobility work only",
                "sparring": ["1-2 light technical rounds early in week", "No hard sparring 4+ days out"],
                "techniques": ["Mental reps", "Light drilling of key techniques"],
                "recovery": "Full recovery focus, hydration, nutrition",
                "mental": mental_prep + ["Confidence building", "Strategy review"]
            }
        }
    elif weeks_remaining >= 6:
        phases = {
            "Phase 1 - Accelerated Build": {
                "duration": f"Weeks 1-{weeks_remaining-4}",
                "focus": f"Rapid skill development targeting opponent weaknesses",
                "training_priorities": training_priorities,
                "conditioning": conditioning_focus[0] if conditioning_focus else "Intense cardio protocol",
                "sparring": sparring_focus[:2],
                "techniques": technique_drills,
                "recovery": "Active recovery, prioritize sleep",
                "mental": ["Begin opponent study", "Visualize success"]
            },
            "Phase 2 - Skill Sharpening": {
                "duration": f"Week {weeks_remaining-3}",
                "focus": "Perfect fight-specific techniques",
                "training_priorities": training_priorities[:3],
                "conditioning": f"Fight pace: {5 if is_five_rounds else 3} full rounds",
                "sparring": sparring_focus,
                "techniques": technique_drills,
                "recovery": "Enhanced recovery protocols",
                "mental": mental_prep
            },
            "Phase 3 - Peak Sparring": {
                "duration": f"Weeks {weeks_remaining-2}-{weeks_remaining-1}",
                "focus": "Fight simulation with opponent-style partners",
                "training_priorities": training_priorities[:2],
                "conditioning": "Maintain peak conditioning",
                "sparring": ["Full fight simulations", "4-5 hard sessions"],
                "techniques": ["Finishing sequences", "Counter setups"],
                "recovery": "Ice baths, massage, full sleep",
                "mental": mental_prep + ["Daily visualization"]
            },
            "Phase 4 - Taper": {
                "duration": "Final Week",
                "focus": "Peak and prepare mentally",
                "training_priorities": ["Light technique", "Stay sharp"],
                "conditioning": "Light movement only",
                "sparring": ["Light technical rounds early in week only"],
                "techniques": ["Mental reps"],
                "recovery": "Full recovery",
                "mental": mental_prep + ["Confidence", "Strategy lock-in"]
            }
        }
    else:
        phases = {
            "Phase 1 - Intensive Prep": {
                "duration": f"Weeks 1-{max(1, weeks_remaining-2)}",
                "focus": f"Aggressive skill development - opponent-specific",
                "training_priorities": training_priorities,
                "conditioning": conditioning_focus[0] if conditioning_focus else "High intensity conditioning",
                "sparring": sparring_focus,
                "techniques": technique_drills,
                "recovery": "Maximize recovery between sessions",
                "mental": mental_prep[:2] if len(mental_prep) > 1 else mental_prep
            },
            "Phase 2 - Peak & Taper": {
                "duration": f"Week {weeks_remaining-1}" if weeks_remaining > 2 else "Days before fight",
                "focus": "Peak performance prep",
                "training_priorities": training_priorities[:2],
                "conditioning": "Fight simulations only",
                "sparring": ["Opponent-style sparring", "1-2 hard sessions"],
                "techniques": ["Key techniques", "Finishing combos"],
                "recovery": "Enhanced recovery",
                "mental": mental_prep + ["Lock in strategy"]
            },
            "Phase 3 - Final Prep": {
                "duration": "Final days",
                "focus": "Stay sharp and confident",
                "training_priorities": ["Light movement", "Mental prep"],
                "conditioning": "None - recover",
                "sparring": ["Light technical only or none"],
                "techniques": ["Mental reps"],
                "recovery": "Full recovery, hydration, nutrition",
                "mental": ["Visualization", "Confidence building", "Execute the plan"]
            }
        }

    return phases


def generate_game_plan(strengths, weaknesses, num_rounds=3):
    strengths_lower = strengths.lower()
    weaknesses_lower = weaknesses.lower()

    striking_offense_keywords = ['striking', 'punching', 'boxing', 'kickboxing', 'muay thai', 'karate', 'knockout power', 'ko power', 'hands', 'kicks', 'elbows', 'knees']
    striking_defense_keywords = ['head movement', 'blocking', 'parrying', 'slipping', 'defensive striking']
    wrestling_keywords = ['wrestling', 'takedowns', 'takedown', 'control', 'cage control', 'clinch', 'dirty boxing']
    bjj_keywords = ['bjj', 'jiu-jitsu', 'jujitsu', 'submissions', 'submission', 'guard', 'ground game', 'chokes', 'armbars']
    grappling_keywords = wrestling_keywords + bjj_keywords + ['grappling', 'ground', 'top control', 'ground and pound', 'gnp']
    cardio_keywords = ['cardio', 'conditioning', 'endurance', 'pace', 'volume', 'gas tank', 'stamina', 'pressure']
    chin_keywords = ['chin', 'durability', 'heart', 'recovery', 'tough', 'iron chin', 'never been ko']
    speed_keywords = ['speed', 'fast', 'quick', 'explosive', 'athleticism', 'athletic']
    power_keywords = ['power', 'knockout', 'ko', 'heavy hands', 'one punch', 'dangerous', 'finisher']
    reach_keywords = ['reach', 'range', 'long', 'length', 'distance']
    pressure_keywords = ['pressure', 'aggression', 'aggressive', 'forward', 'volume', 'relentless']
    counter_keywords = ['counter', 'timing', 'patient', 'reads', 'counter striker', 'counter puncher']
    experience_keywords = ['experienced', 'veteran', 'smart', 'iq', 'fight iq', 'crafty']

    opp_striking_offense = any(keyword in strengths_lower for keyword in striking_offense_keywords)
    opp_striking_defense = any(keyword in strengths_lower for keyword in striking_defense_keywords)
    opp_wrestling = any(keyword in strengths_lower for keyword in wrestling_keywords)
    opp_bjj = any(keyword in strengths_lower for keyword in bjj_keywords)
    opp_grappling = any(keyword in strengths_lower for keyword in grappling_keywords)
    opp_cardio = any(keyword in strengths_lower for keyword in cardio_keywords)
    opp_chin = any(keyword in strengths_lower for keyword in chin_keywords)
    opp_speed = any(keyword in strengths_lower for keyword in speed_keywords)
    opp_power = any(keyword in strengths_lower for keyword in power_keywords)
    opp_reach = any(keyword in strengths_lower for keyword in reach_keywords)
    opp_pressure = any(keyword in strengths_lower for keyword in pressure_keywords)
    opp_counter = any(keyword in strengths_lower for keyword in counter_keywords)
    opp_experience = any(keyword in strengths_lower for keyword in experience_keywords)

    weak_striking = any(keyword in weaknesses_lower for keyword in striking_offense_keywords + striking_defense_keywords)
    weak_wrestling = any(keyword in weaknesses_lower for keyword in wrestling_keywords)
    weak_bjj = any(keyword in weaknesses_lower for keyword in bjj_keywords)
    weak_grappling = any(keyword in weaknesses_lower for keyword in grappling_keywords)
    weak_cardio = any(keyword in weaknesses_lower for keyword in cardio_keywords)
    weak_chin = any(keyword in weaknesses_lower for keyword in chin_keywords)
    weak_speed = any(keyword in weaknesses_lower for keyword in speed_keywords)
    weak_pressure = any(keyword in weaknesses_lower for keyword in pressure_keywords)
    weak_counter = any(keyword in weaknesses_lower for keyword in counter_keywords)
    weak_defense = any(keyword in weaknesses_lower for keyword in ['defense', 'defensive', 'blocking', 'guard'])
    weak_tdd = any(keyword in weaknesses_lower for keyword in ['tdd', 'takedown defense', 'gets taken down', 'wrestling defense'])

    strategic_approach = []
    tactical_notes = []
    techniques_to_drill = []
    things_to_avoid = []

    if opp_grappling and weak_striking:
        preferred_range = "Striking (Stay Standing)"
        range_reason = "Opponent is dangerous on the ground but vulnerable on the feet - keep it standing and outstrike them"
        strategic_approach.append("Maintain distance and use footwork to avoid clinch/takedowns")
        strategic_approach.append("Punish with strikes when opponent reaches for takedowns")
        strategic_approach.append("Use front kicks and teeps to manage distance")
        techniques_to_drill.extend(["Takedown defense", "Sprawl to strikes", "Jab and move", "Lateral footwork", "Uppercuts on level changes"])
        things_to_avoid.extend(["Clinching unnecessarily", "Fighting against the cage", "Going to the ground", "Getting too close"])

    elif opp_striking_offense and weak_grappling:
        preferred_range = "Wrestling & Ground"
        range_reason = "Opponent is dangerous on the feet but weak on the ground - take them down and control"
        strategic_approach.append("Close distance quickly to avoid getting hit")
        strategic_approach.append("Shoot takedowns early to establish dominance")
        strategic_approach.append("Use clinch work against the cage to set up takedowns")
        techniques_to_drill.extend(["Level change shots", "Double leg", "Single leg to high crotch", "Cage wrestling", "Ground and pound"])
        things_to_avoid.extend(["Trading punches at range", "Fighting at kicking distance", "Prolonged striking exchanges", "Standing and banging"])

    elif opp_striking_offense and weak_wrestling:
        preferred_range = "Clinch & Wrestling"
        range_reason = "Opponent can strike but can't defend takedowns - wrestle them relentlessly"
        strategic_approach.append("Shoot early and often to establish the threat")
        strategic_approach.append("Use clinch against cage to drain energy and land takedowns")
        strategic_approach.append("Mix in ground and pound to maximize damage")
        techniques_to_drill.extend(["Chain wrestling", "Clinch takedowns", "Cage wrestling", "Top control", "Ground and pound"])
        things_to_avoid.extend(["Standing in the pocket", "Kickboxing range", "Getting baited into striking"])

    elif weak_tdd:
        preferred_range = "Wrestling (Takedown Focus)"
        range_reason = "Opponent has poor takedown defense - use wrestling to control the fight"
        strategic_approach.append("Level change frequently to keep opponent guessing")
        strategic_approach.append("Use strikes to set up takedowns")
        strategic_approach.append("Once on top, maintain control and land ground strikes")
        techniques_to_drill.extend(["Setups from strikes to shots", "Double leg", "High crotch", "Body lock takedowns", "Ground and pound"])
        things_to_avoid.extend(["Abandoning wrestling if first attempts fail", "Staying on feet too long", "Pulling guard"])

    elif opp_wrestling and weak_striking:
        preferred_range = "Striking (Anti-Wrestling)"
        range_reason = "Opponent wants to wrestle but can't strike - stuff takedowns and light them up"
        strategic_approach.append("Focus heavily on takedown defense")
        strategic_approach.append("Punish every shot attempt with uppercuts and knees")
        strategic_approach.append("Use footwork to stay off the cage")
        techniques_to_drill.extend(["Sprawl and brawl", "Uppercuts on level changes", "Knees in clinch", "Cage getups", "Circling footwork"])
        things_to_avoid.extend(["Getting backed to the cage", "Giving up underhooks", "Going to the ground", "Extended clinch battles"])

    elif weak_cardio and opp_power:
        preferred_range = "Striking (Volume Later)"
        range_reason = "Opponent has power but fades - survive early rounds and pour it on when they gas"
        strategic_approach.append("Be defensively responsible in early rounds")
        strategic_approach.append("Use movement and avoid big exchanges early")
        strategic_approach.append("Increase output dramatically as opponent slows")
        strategic_approach.append("Target body shots to speed up fatigue")
        techniques_to_drill.extend(["Defensive footwork", "Body combinations", "Volume combos", "Cardio conditioning"])
        things_to_avoid.extend(["Wild exchanges in round 1", "Getting into a brawl early", "Standing directly in front"])

    elif weak_chin:
        preferred_range = "Striking (Power Shots)"
        range_reason = "Opponent can be hurt - set up clean power shots and look for the finish"
        strategic_approach.append("Be patient and set up power shots properly")
        strategic_approach.append("Use feints and combinations to create openings")
        strategic_approach.append("When opponent is hurt, stay composed and finish")
        techniques_to_drill.extend(["Power combinations", "Hooks to the chin", "Overhand rights", "Body-head combos", "Finishing sequences"])
        things_to_avoid.extend(["Rushing in recklessly", "Loading up too obviously", "Getting wild when opponent is hurt"])

    elif opp_counter and weak_pressure:
        preferred_range = "Pressure Striking"
        range_reason = "Opponent waits to counter but wilts under pressure - take the fight to them"
        strategic_approach.append("Apply constant forward pressure")
        strategic_approach.append("Force opponent to lead and make mistakes")
        strategic_approach.append("Cut off the cage and limit movement")
        techniques_to_drill.extend(["Jab-cross while moving forward", "Cage cutting", "Body shots", "Feints to draw counters"])
        things_to_avoid.extend(["Waiting and giving opponent time", "Fighting at range", "Being passive"])

    elif opp_pressure and weak_counter:
        preferred_range = "Counter Striking"
        range_reason = "Opponent is aggressive but leaves openings - make them pay for coming forward"
        strategic_approach.append("Use footwork to create angles")
        strategic_approach.append("Time counters as opponent rushes in")
        strategic_approach.append("Use push kicks and teeps to manage distance")
        techniques_to_drill.extend(["Counter hooks", "Pull counters", "Check hooks while moving", "Teep kicks"])
        things_to_avoid.extend(["Getting backed against the cage", "Engaging in brawls", "Matching their pace"])

    elif opp_bjj and weak_wrestling:
        preferred_range = "Standing or Top Control"
        range_reason = "Opponent is dangerous on the ground but can't get there - keep it standing or stay on top"
        strategic_approach.append("Stuff takedowns and punish attempts")
        strategic_approach.append("If fight goes to ground, maintain top position at all costs")
        strategic_approach.append("Use ground and pound from top, don't pass into submissions")
        techniques_to_drill.extend(["Takedown defense", "Top control", "Ground and pound", "Safe guard passing"])
        things_to_avoid.extend(["Pulling guard", "Giving up your back", "Diving into submission attempts"])

    elif opp_reach and weak_speed:
        preferred_range = "Close Range / Pocket"
        range_reason = "Opponent has reach advantage but is slow - close distance and fight inside"
        strategic_approach.append("Use head movement to slip inside their range")
        strategic_approach.append("Fight in the pocket where reach doesn't matter")
        strategic_approach.append("Use speed advantage to land first")
        techniques_to_drill.extend(["Slipping punches", "Inside fighting combos", "Hooks and uppercuts", "Clinch entries"])
        things_to_avoid.extend(["Fighting at kicking range", "Backing up straight", "Letting opponent jab from distance"])

    elif weak_cardio:
        preferred_range = "High Volume (Any Range)"
        range_reason = "Opponent has cardio issues - push a relentless pace and break them"
        strategic_approach.append("Start with high output from round 1")
        strategic_approach.append("Never let opponent rest - constant activity")
        strategic_approach.append("Target body to accelerate fatigue")
        techniques_to_drill.extend(["Body combinations", "Volume striking", "Clinch work", "Pressure fighting"])
        things_to_avoid.extend(["Giving opponent rest", "Slow pacing", "Long breaks between attacks"])

    elif weak_defense:
        preferred_range = "Striking (Volume)"
        range_reason = "Opponent is defensively porous - overwhelm them with volume"
        strategic_approach.append("High output striking from the start")
        strategic_approach.append("Use long combinations")
        strategic_approach.append("Mix attacks to all targets")
        techniques_to_drill.extend(["5-6 punch combinations", "Body-head combinations", "Follow-up attacks", "Pressure"])
        things_to_avoid.extend(["Single shots", "Being passive", "Letting opponent dictate pace"])

    else:
        preferred_range = "Mixed Martial Arts"
        range_reason = "Balanced approach - use all tools and adapt based on what's working"
        strategic_approach.append("Test opponent's reactions in multiple ranges")
        strategic_approach.append("Adapt strategy based on what's working")
        strategic_approach.append("Look for openings and capitalize")
        techniques_to_drill.extend(["Basic combinations", "Takedown offense/defense", "Ground transitions"])
        things_to_avoid.extend(["One-dimensional fighting", "Predictable patterns", "Ignoring what's working"])

    if opp_power and opp_speed:
        tactical_notes.append("⚠️ HIGH DANGER: Opponent is fast AND powerful - extreme caution in exchanges")
        things_to_avoid.append("Trading power shots")
    if weak_cardio:
        tactical_notes.append("📈 LATE ROUND OPPORTUNITY: Opponent fades - increase output after round 2")
    if opp_cardio and opp_pressure:
        tactical_notes.append("⏰ LONG FIGHT: Prepare for a grueling pace - prioritize your conditioning")
    if weak_chin and weak_defense:
        tactical_notes.append("🎯 FINISH OPPORTUNITY: Opponent is hittable - look for the stoppage")
    if opp_experience:
        tactical_notes.append("🧠 SMART OPPONENT: Expect adjustments - have backup plans ready")
    if weak_tdd:
        tactical_notes.append("🤼 WRESTLING OPPORTUNITY: Opponent can be taken down - mix in shots")

    round_objectives = {}

    if num_rounds == 3:
        if "Striking" in preferred_range or preferred_range == "Counter Striking" or preferred_range == "Pressure Striking":
            if opp_grappling or opp_wrestling:
                round_objectives = {
                    "Round 1": {
                        "objective": "Establish striking and stuff takedowns",
                        "tactics": f"Circle away from power side. Use jab to maintain distance. When they shoot: sprawl hard, get back up immediately. Land strikes as they close distance. {techniques_to_drill[0] if techniques_to_drill else 'Use footwork'}.",
                        "target": "Prove you can stop their wrestling and hurt them on the feet"
                    },
                    "Round 2": {
                        "objective": "Increase striking output with TDD confidence",
                        "tactics": "You've shown you can stop takedowns. Now start sitting down on shots. Look for counters when they level change - uppercuts and knees. Make them pay for every failed attempt.",
                        "target": "Win round clearly on the feet, punish takedown attempts"
                    },
                    "Round 3": {
                        "objective": "Dominate standing or get the finish",
                        "tactics": "Opponent should be frustrated. Either they keep shooting (stuff and strike) or they try to stand with you (where you're better). If they're hurt, stay composed and finish. Don't get taken down late.",
                        "target": "Finish or clear decision - DO NOT get taken down"
                    }
                }
            elif weak_chin:
                round_objectives = {
                    "Round 1": {
                        "objective": "Find timing and test the chin",
                        "tactics": "Patient approach. Use jab to find range. Set traps with feints. Land 2-3 clean power shots to see how they react. Watch for signs they're hurt (legs wobble, hands drop, backing up).",
                        "target": "Establish timing, land clean, see how they respond to power"
                    },
                    "Round 2": {
                        "objective": "Increase power and look for the hurt",
                        "tactics": "You have the timing now. Start sitting down on hooks and overhands. Use body shots to bring hands down, then go upstairs. When you hurt them - STAY COMPOSED - don't rush in wild.",
                        "target": "Hurt opponent and look for finish opportunity"
                    },
                    "Round 3": {
                        "objective": "Close the show",
                        "tactics": "If they're still standing, they've taken damage. Accumulated damage catches up. Set up your best power shot and let it go. If you hurt them, swarm intelligently - punches in bunches.",
                        "target": "Get the knockout or dominant decision"
                    }
                }
            elif weak_cardio:
                round_objectives = {
                    "Round 1": {
                        "objective": "Set a pace they can't maintain",
                        "tactics": "High output from the start. Throw in bunches, not single shots. Target the body to accelerate fatigue. Make them work defensively. Don't overcommit - save energy for later.",
                        "target": "Win round and start draining their gas tank"
                    },
                    "Round 2": {
                        "objective": "Increase pressure as they slow",
                        "tactics": "Watch for signs of fatigue: hands dropping, mouth open, slower reactions. Push the pace even harder. Body shots continue. Cut off the cage - don't let them rest.",
                        "target": "Dominate a slowing opponent"
                    },
                    "Round 3": {
                        "objective": "Break them or cruise to victory",
                        "tactics": "They should be exhausted. Either pour it on for the finish or fight smart to secure decision. If they're still fighting back, you have the cardio advantage - use it.",
                        "target": "Finish the fight or clear 30-27 decision"
                    }
                }
            elif opp_counter:
                round_objectives = {
                    "Round 1": {
                        "objective": "Force them to lead",
                        "tactics": "Constant forward pressure but with feints first. Make them throw first, then counter their counter. Cut off cage - don't let them circle. Use feints to make them flinch.",
                        "target": "Take their game away - don't let them wait and counter"
                    },
                    "Round 2": {
                        "objective": "Increase pressure and volume",
                        "tactics": "They're uncomfortable being the aggressor. Push harder. Body shots to slow their movement. Throw combinations, not single shots that they can time.",
                        "target": "Overwhelm with pressure"
                    },
                    "Round 3": {
                        "objective": "Maintain pressure for finish or decision",
                        "tactics": "Stay on them. If you've been pressuring correctly, they should be out of rhythm. Look for openings as frustration sets in.",
                        "target": "Secure victory through pressure"
                    }
                }
            else:
                round_objectives = {
                    "Round 1": {
                        "objective": "Establish range and timing",
                        "tactics": f"Use jab to find distance. Look for opponent's patterns and tells. {strategic_approach[0] if strategic_approach else 'Implement game plan'}. Stay defensively responsible.",
                        "target": "Download opponent and win round"
                    },
                    "Round 2": {
                        "objective": "Exploit what you've learned",
                        "tactics": "You know their timing now. Start capitalizing on openings. If something's working, do more of it. Make adjustments if they adapted.",
                        "target": "Build on round 1 success"
                    },
                    "Round 3": {
                        "objective": "Close the fight",
                        "tactics": "If ahead, fight smart but don't coast. If behind, increase output and take calculated risks. Leave no doubt.",
                        "target": "Finish or secure clear decision"
                    }
                }

        elif "Wrestling" in preferred_range or "Ground" in preferred_range or "Clinch" in preferred_range:
            if opp_striking_offense:
                round_objectives = {
                    "Round 1": {
                        "objective": "Get to the clinch/ground FAST",
                        "tactics": "Close distance quickly behind a jab or level change. Don't hang out at striking range. Once you touch them, stay attached. Cage them up for the takedown. First takedown is crucial for confidence.",
                        "target": "Establish wrestling dominance, minimize time on feet"
                    },
                    "Round 2": {
                        "objective": "Continue wrestling domination",
                        "tactics": "They know takedowns are coming but can't stop them. Mix up your shots. Ground and pound to accumulate damage. Don't give up position for submissions - stay in control.",
                        "target": "Control time and damage from top"
                    },
                    "Round 3": {
                        "objective": "Finish or grind out the win",
                        "tactics": "Opponent should be demoralized from being controlled. Either look for a finish (GnP or submission) or ride out the decision. DO NOT stand and bang out of ego.",
                        "target": "Finish or 30-27 via control"
                    }
                }
            elif weak_tdd:
                round_objectives = {
                    "Round 1": {
                        "objective": "Expose the TDD weakness immediately",
                        "tactics": "Shoot early to plant the seed of doubt. Once you're on top, stay heavy and work ground and pound. Every takedown breaks their spirit more.",
                        "target": "Multiple takedowns, establish complete dominance"
                    },
                    "Round 2": {
                        "objective": "Accumulate damage and control",
                        "tactics": "They're in survival mode now. Chain your wrestling - when they stand up, take them back down. Ground and pound to damage or open submissions.",
                        "target": "Total domination, look for finish"
                    },
                    "Round 3": {
                        "objective": "Get the finish or cruise",
                        "tactics": "You should have 8+ minutes of control. Either find the stoppage via GnP or submission, or secure the easy decision. Don't get complacent.",
                        "target": "Finish or lopsided decision"
                    }
                }
            elif weak_grappling:
                round_objectives = {
                    "Round 1": {
                        "objective": "Get top position and keep it",
                        "tactics": "Take fight to the ground by any means - shot, clinch, trip. Once on top, prioritize control over damage initially. Let them carry your weight.",
                        "target": "Establish ground superiority"
                    },
                    "Round 2": {
                        "objective": "Increase damage from top",
                        "tactics": "You've proven you can hold them down. Now start opening up with ground strikes. Pass guard to more dominant positions. Look for submission setups.",
                        "target": "Ground and pound damage, advance position"
                    },
                    "Round 3": {
                        "objective": "Close the show from top",
                        "tactics": "Maximum damage within control. If submission is there, take it. If not, pound them out or ride the decision. They have no answer for you on the ground.",
                        "target": "Finish or dominant decision"
                    }
                }
            else:
                round_objectives = {
                    "Round 1": {
                        "objective": "Establish the takedown threat",
                        "tactics": f"{strategic_approach[0] if strategic_approach else 'Get to the clinch and work for takedowns'}. First takedown sets the tone. Control from top position.",
                        "target": "Win round with wrestling"
                    },
                    "Round 2": {
                        "objective": "Continue wrestling attacks",
                        "tactics": "Mix up shots and clinch work. Ground and pound when on top. Don't let them establish anything standing.",
                        "target": "Extend wrestling dominance"
                    },
                    "Round 3": {
                        "objective": "Wrestling to victory",
                        "tactics": "You've proven superiority. Finish via GnP or submission, or cruise to decision on control time.",
                        "target": "Secure victory"
                    }
                }

        elif opp_power:
            round_objectives = {
                "Round 1": {
                    "objective": "SURVIVE - Don't get hit clean",
                    "tactics": "Maximum defense. Head movement, footwork, hands up at all times. Download their timing and patterns. Don't trade. Avoid their power hand. Win round on points if possible, but survival is priority.",
                    "target": "Get through round without taking big shots"
                },
                "Round 2": {
                    "objective": "Start countering safely",
                    "tactics": "You know their timing now. Start picking them apart with counters. Still don't trade - hit and move. Their power should be consistent, but your timing gives you an edge now.",
                    "target": "Win round while staying safe"
                },
                "Round 3": {
                    "objective": "Outwork for decision",
                    "tactics": "If you've avoided their power, you should have the cardio edge. Increase output now. They may be frustrated from missing. Stay disciplined but up the volume.",
                    "target": "Clear round win for decision"
                }
            }

        else:
            round_objectives = {
                "Round 1": {
                    "objective": "Implement the game plan",
                    "tactics": f"{strategic_approach[0] if strategic_approach else 'Execute primary strategy'}. {strategic_approach[1] if len(strategic_approach) > 1 else 'Stay focused on what works'}.",
                    "target": "Win round and establish your game"
                },
                "Round 2": {
                    "objective": "Adapt and dominate",
                    "tactics": "Double down on what's working. Make adjustments if opponent adapted. Don't let them back in the fight.",
                    "target": "Extend your lead"
                },
                "Round 3": {
                    "objective": "Finish strong",
                    "tactics": "If ahead, smart fighting. If behind, increase risk. Leave no doubt about the winner.",
                    "target": "Secure victory"
                }
            }

    else:  # 5 rounds
        if "Striking" in preferred_range and (opp_grappling or opp_wrestling):
            round_objectives = {
                "Round 1": {"objective": "Establish anti-wrestling", "tactics": "Stuff takedowns, land strikes when they shoot. Prove you can't be taken down.", "target": "Set the tone on the feet"},
                "Round 2": {"objective": "Increase striking confidence", "tactics": "Start sitting down on shots. They're hesitant to shoot now.", "target": "Damage accumulation"},
                "Round 3": {"objective": "Championship round - break them", "tactics": "This is where fights are won. Push pace and punish them.", "target": "Take over the fight"},
                "Round 4": {"objective": "Pour it on", "tactics": "If you've stopped their wrestling, they're demoralized. Volume up.", "target": "Look for finish"},
                "Round 5": {"objective": "Close the show", "tactics": "Smart if ahead, aggressive if close. Don't get taken down now.", "target": "Victory"}
            }
        elif "Wrestling" in preferred_range or "Ground" in preferred_range:
            round_objectives = {
                "Round 1": {"objective": "First takedown", "tactics": "Get to the ground early. Establish you can put them down.", "target": "Control time"},
                "Round 2": {"objective": "Maintain wrestling", "tactics": "Continue taking them down. Ground and pound damage.", "target": "Accumulate control and damage"},
                "Round 3": {"objective": "Championship round grind", "tactics": "This is where your wrestling conditioning matters. Keep grinding.", "target": "Break their will"},
                "Round 4": {"objective": "Finish or cruise", "tactics": "They're demoralized from being controlled. Look for submission or TKO.", "target": "Stoppage opportunity"},
                "Round 5": {"objective": "Secure victory", "tactics": "One more takedown and ride. Don't let them up for a hail mary.", "target": "Dominant decision or finish"}
            }
        elif weak_cardio:
            round_objectives = {
                "Round 1": {"objective": "Set the pace", "tactics": "High output to start the drain. Target body.", "target": "Begin fatigue process"},
                "Round 2": {"objective": "Maintain pace", "tactics": "Don't let them rest. Continue body work.", "target": "Watch for fatigue signs"},
                "Round 3": {"objective": "Break point", "tactics": "This is where they should crack. Increase pressure.", "target": "Look for finish"},
                "Round 4": {"objective": "Capitalize on exhaustion", "tactics": "Pour it on. They have nothing left.", "target": "Finish or dominate"},
                "Round 5": {"objective": "Coast or finish", "tactics": "Easy work if they're broken. Don't let up completely.", "target": "Secure victory"}
            }
        elif weak_chin:
            round_objectives = {
                "Round 1": {"objective": "Find timing", "tactics": "Patient, set up power shots. Test the chin.", "target": "Establish range"},
                "Round 2": {"objective": "Increase power", "tactics": "You have the timing. Start loading up.", "target": "Hurt opponent"},
                "Round 3": {"objective": "Hunt the knockout", "tactics": "Championship rounds - time to find it.", "target": "Finish opportunity"},
                "Round 4": {"objective": "Close the show", "tactics": "Accumulated damage. Set up your best shot.", "target": "Get the knockout"},
                "Round 5": {"objective": "Final push", "tactics": "If still standing, go all out for finish.", "target": "Finish or clear decision"}
            }
        else:
            round_objectives = {
                "Round 1": {"objective": "Download and establish", "tactics": f"{strategic_approach[0] if strategic_approach else 'Implement game plan'}. Learn opponent's patterns.", "target": "Win round"},
                "Round 2": {"objective": "Build momentum", "tactics": "Capitalize on what you learned. Extend the lead.", "target": "Dominate"},
                "Round 3": {"objective": "Championship round", "tactics": "This is where champions are made. Push through.", "target": "Show heart"},
                "Round 4": {"objective": "Break their will", "tactics": "You've imposed your game. Now finish the job.", "target": "Look for finish"},
                "Round 5": {"objective": "Finish strong", "tactics": "Leave it all in there. No regrets.", "target": "Secure victory"}
            }

    return {
        'preferred_range': preferred_range,
        'range_reason': range_reason,
        'strategic_approach': strategic_approach,
        'tactical_notes': tactical_notes,
        'techniques_to_drill': techniques_to_drill,
        'things_to_avoid': things_to_avoid,
        'round_objectives': round_objectives
    }


@training_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = FighterProfileForm()
    fighter_profile = FighterProfile.query.filter_by(user_id=current_user.id).first()
    if request.method == 'GET' and fighter_profile:
        form.age.data = fighter_profile.age
        form.height.data = fighter_profile.height
        form.walk_around_weight.data = fighter_profile.walk_around_weight
        form.weight_class.data = fighter_profile.weight_class
        form.fight_date.data = fighter_profile.fight_date
        form.training_availability.data = fighter_profile.training_availability
        form.se_angle.data = fighter_profile.se_angle

    if form.validate_on_submit():
        if form.profile_picture.data:
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            filename = secure_filename(f"{current_user.id}_{form.profile_picture.data.filename}")
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.profile_picture.data.save(file_path)
            current_user.profile_picture = f"uploads/{filename}"

        if fighter_profile:
            fighter_profile.age = form.age.data
            fighter_profile.height = form.height.data
            fighter_profile.walk_around_weight = form.walk_around_weight.data
            fighter_profile.weight_class = form.weight_class.data
            fighter_profile.fight_date = form.fight_date.data
            fighter_profile.training_availability = form.training_availability.data
            fighter_profile.se_angle = form.se_angle.data
        else:
            new_profile = FighterProfile(
                user_id=current_user.id,
                age=form.age.data,
                height=form.height.data,
                walk_around_weight=form.walk_around_weight.data,
                weight_class=form.weight_class.data,
                fight_date=form.fight_date.data,
                training_availability=form.training_availability.data,
                se_angle=form.se_angle.data
            )
            db.session.add(new_profile)
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('main.dashboard'))

    return render_template('profile.html', form=form)


@training_bp.route('/camp_planner', methods=['GET', 'POST'])
@login_required
def camp_planner():
    form = CampPlanForm()
    fighter_profile = FighterProfile.query.filter_by(user_id=current_user.id).first()
    if not fighter_profile:
        flash('Please complete your fighter profile first')
        return redirect(url_for('training.profile'))

    today = datetime.today().date()
    weeks_remaining = max(1, (fighter_profile.fight_date - today).days // 7)

    if form.validate_on_submit():
        plan_details = generate_camp_plan(
            form.opponent_strengths.data,
            form.opponent_weaknesses.data,
            weeks_remaining,
            form.fight_type.data
        )

        plan = CampPlan(
            user_id=current_user.id,
            weeks_remaining=weeks_remaining,
            fight_type=form.fight_type.data,
            opponent_name=form.opponent_name.data or "Unknown Opponent",
            opponent_strengths=form.opponent_strengths.data,
            opponent_weaknesses=form.opponent_weaknesses.data,
            plan_phases=json.dumps(plan_details)
        )
        db.session.add(plan)
        db.session.commit()
        flash('Detailed opponent-specific camp plan generated successfully!')
        return redirect(url_for('training.view_camp_plans'))

    return render_template('camp_planner.html', form=form, weeks_remaining=weeks_remaining)


@training_bp.route('/game_plan', methods=['GET', 'POST'])
@login_required
def game_plan():
    form = GamePlanForm()

    fighter_id = request.args.get('fighter_id', type=int)
    fighter = Fighter.query.get(fighter_id) if fighter_id else None

    if fighter and request.method == 'GET':
        form.opponent_strengths.data = fighter.strengths or ''
        form.opponent_weaknesses.data = fighter.weaknesses or ''

    if form.validate_on_submit():
        num_rounds = int(form.fight_rounds.data)

        strengths = fighter.strengths if fighter else form.opponent_strengths.data
        weaknesses = fighter.weaknesses if fighter else form.opponent_weaknesses.data

        plan_data = generate_game_plan(strengths, weaknesses, num_rounds)

        full_plan = {
            'strategic_approach': plan_data['strategic_approach'],
            'tactical_notes': plan_data['tactical_notes'],
            'techniques_to_drill': plan_data['techniques_to_drill'],
            'things_to_avoid': plan_data['things_to_avoid'],
            'range_reason': plan_data['range_reason'],
            'round_objectives': plan_data['round_objectives']
        }

        plan = GamePlan(
            user_id=current_user.id,
            opponent_strengths=strengths,
            opponent_weaknesses=weaknesses,
            preferred_range=plan_data['preferred_range'],
            round_objectives=json.dumps(full_plan),
            opponent_name=fighter.name if fighter else None
        )
        db.session.add(plan)
        db.session.commit()

        flash('Comprehensive Game Plan generated successfully!')
        return redirect(url_for('training.view_game_plans'))

    return render_template('game_plan.html', form=form, generated_plan=None, fighter=fighter)


@training_bp.route('/weight_tracker', methods=['GET', 'POST'])
@login_required
def weight_tracker():
    form = WeightLogForm()
    if form.validate_on_submit():
        log = WeightLog(
            user_id=current_user.id,
            date=datetime.today().date(),
            weight=form.weight.data
        )
        db.session.add(log)
        db.session.commit()
        flash('Weight logged successfully', 'success')
        return redirect(url_for('training.weight_tracker'))
    elif request.method == 'POST':
        flash('Please enter a valid weight between 100 and 400 lbs.', 'danger')

    logs = WeightLog.query.filter_by(user_id=current_user.id).order_by(WeightLog.date.desc()).all()

    fighter_profile = FighterProfile.query.filter_by(user_id=current_user.id).first()
    score = None
    if fighter_profile and logs:
        target_weight = fighter_profile.walk_around_weight - 10
        current_weight = logs[0].weight
        weight_trend = "Stable"
        if len(logs) > 1:
            recent_avg = sum(log.weight for log in logs[:7]) / min(7, len(logs))
            older_avg = sum(log.weight for log in logs[7:14]) / min(7, len(logs[7:])) if len(logs) > 7 else recent_avg
            if recent_avg < older_avg:
                weight_trend = "Decreasing"
            elif recent_avg > older_avg:
                weight_trend = "Increasing"

        risks = []
        weekly_loss = 2
        if weight_trend == "Decreasing" and len(logs) > 7:
            loss_rate = (older_avg - recent_avg) / 1
            if loss_rate > weekly_loss:
                risks.append("Weight loss rate exceeds safe threshold")
        if current_weight > target_weight + 5:
            risks.append("Projected cut may not be achievable")

        score = 100
        weight_diff = current_weight - target_weight
        if weight_diff > 5:
            score -= min(80, weight_diff * 3)  # 3 points per lb over, max 80 deduction
        elif weight_diff > 0:
            score -= 10

        if fighter_profile.training_availability < 3:
            score -= 20
        elif fighter_profile.training_availability < 5:
            score -= 10

        if not CampPlan.query.filter_by(user_id=current_user.id).count():
            score -= 15

        days_until = (fighter_profile.fight_date - datetime.today().date()).days
        if days_until <= 14:
            score -= 20
        elif days_until <= 30:
            score -= 10
        elif days_until <= 60:
            score -= 5

        score = max(0, score)
        risk_level = "High" if score < 30 else "Medium" if score < 70 else "Low"
    else:
        weight_trend = "No data"
        risks = []
        risk_level = "Unknown"

    return render_template('weight_tracker.html', form=form, logs=logs, weight_trend=weight_trend,
                           risks=risks, risk_level=risk_level, score=score)


@training_bp.route('/risk_readiness')
@login_required
def risk_readiness():
    fighter_profile = FighterProfile.query.filter_by(user_id=current_user.id).first()
    if not fighter_profile:
        flash('Please complete your fighter profile first')
        return redirect(url_for('training.profile'))

    score = 100
    factors = []

    latest_weight = WeightLog.query.filter_by(user_id=current_user.id).order_by(WeightLog.date.desc()).first()
    if latest_weight:
        target = fighter_profile.walk_around_weight - 10
        weight_diff = latest_weight.weight - target
        if weight_diff <= 0:
            factors.append("Weight on track (no deduction)")
        elif weight_diff <= 5:
            score -= 10
            factors.append("Weight close to target (-10)")
        else:
            weight_penalty = min(80, weight_diff * 3)
            score -= weight_penalty
            factors.append(f"Weight over target (-{weight_penalty})")

    if fighter_profile.training_availability < 3:
        score -= 20
        factors.append("Low training availability (-20)")
    elif fighter_profile.training_availability < 5:
        score -= 10
        factors.append("Moderate training availability (-10)")

    if not CampPlan.query.filter_by(user_id=current_user.id).count():
        score -= 15
        factors.append("No camp plan (-15)")

    days_until = (fighter_profile.fight_date - datetime.today().date()).days
    if days_until > 60:
        factors.append("Sufficient time to fight (no deduction)")
    elif days_until > 30:
        score -= 5
        factors.append("Moderate time to fight (-5)")
    elif days_until > 14:
        score -= 10
        factors.append("Limited time to fight (-10)")
    else:
        score -= 20
        factors.append("Very close to fight (-20)")

    score = max(0, score)
    readiness_level = "Low" if score < 30 else "Medium" if score < 70 else "High"
    risk_level = "High" if score < 30 else "Medium" if score < 70 else "Low"

    return render_template('risk_readiness.html', score=score, readiness_level=readiness_level,
                           risk_level=risk_level, factors=factors)


@training_bp.route('/view_camp_plans')
@login_required
def view_camp_plans():
    camp_plans = CampPlan.query.filter_by(user_id=current_user.id).order_by(CampPlan.id.desc()).all()
    return render_template('view_camp_plans.html', camp_plans=camp_plans)


@training_bp.route('/view_game_plans')
@login_required
def view_game_plans():
    game_plans = GamePlan.query.filter_by(user_id=current_user.id).order_by(GamePlan.id.desc()).all()
    return render_template('view_game_plans.html', game_plans=game_plans)


@training_bp.route('/delete_camp_plan/<int:plan_id>', methods=['POST'])
@login_required
def delete_camp_plan(plan_id):
    plan = CampPlan.query.filter_by(id=plan_id, user_id=current_user.id).first()
    if plan:
        db.session.delete(plan)
        db.session.commit()
        flash('Camp plan deleted successfully')
    else:
        flash('Camp plan not found')
    return redirect(url_for('training.view_camp_plans'))


@training_bp.route('/delete_game_plan/<int:plan_id>', methods=['POST'])
@login_required
def delete_game_plan(plan_id):
    plan = GamePlan.query.filter_by(id=plan_id, user_id=current_user.id).first()
    if plan:
        db.session.delete(plan)
        db.session.commit()
        flash('Game plan deleted successfully')
    else:
        flash('Game plan not found')
    return redirect(url_for('training.view_game_plans'))


@training_bp.route('/delete_weight_log/<int:log_id>', methods=['POST'])
@login_required
def delete_weight_log(log_id):
    log = WeightLog.query.filter_by(id=log_id, user_id=current_user.id).first()
    if log:
        db.session.delete(log)
        db.session.commit()
        flash('Weight log deleted successfully')
    else:
        flash('Weight log not found')
    return redirect(url_for('training.weight_tracker'))
