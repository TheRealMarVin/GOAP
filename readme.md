# 🧠 **GOAP** 🎉

## What is this madness?

If you’ve ever wanted your NPCs to stop being headless chickens and make decisions like a semi-functional adult (or at least a squirrel with a plan), you’re in the right place!

Welcome to a wild ride through the basics of **GOAP (Goal-Oriented Action Planning)**, where your friendly AI agents will decide not just *what* to do, but *how* to do it, all while looking surprisingly competent!

This project is the first step toward world domination… or maybe just getting your AI to actually finish cooking their virtual food before the fire goes out. 🥘🔥

The goal? **Understanding the basics of GOAP** so you can experiment, tweak, break things, and eventually create NPCs that *almost* act like real people. Why? Because we can, that's why! 😎

---

## 🤖 Project Overview

This is a GOAP crash course (at least for me), designed to help you dive headfirst into the wonderful world of AI planning systems. With this project, you’ll learn how to:

- Set **goals** for your agents (from "gather wood" to "cook food" to "run away from the terrifying spider" 🕷️).
- Define **actions** with fancy stuff like preconditions and effects, because NPCs like to feel smart, too.
- See how our agents deal with a *dynamic world* where their goals might change halfway through (like when they suddenly realize there’s a boss fight looming... 😱).

With this foundational setup, you'll be ready to start building more complex behaviors, like NPCs that can navigate chaotic environments, handle unexpected events, or even develop a love for firewood gathering (hey, we don’t judge their hobbies!).

### 🍳 Cooking Task Goal
The goal of the cooking task is to collect ingredients, prepare meals, and cook a delicious dish within a virtual environment. Our GOAP agent will plan actions such as gathering ingredients, starting a fire, or waiting for the food to cook. The objective is to achieve a cooked meal while managing limited resources like time and ingredients.

### ⚔️ Fighting Task Goal
In the fighting task, our agent aims to eliminate all enemies in the environment. During execution, the agent moves strategically to get into range of enemies and waits for the right moment to strike. The agent must manage stamina and health, positioning itself carefully while anticipating attacks and delivering blows when the opportunity arises.

The ultimate goal is to defeat all enemies that are moving to improve survival. There are two agents: one moves horizontally back and forth across the grid, while the other moves vertically.


---

## 📦 Installation & Requirements

To run this glorious GOAP experiment, you don’t need anything fancy—just your average **Python** environment and a dash of curiosity!

### Step 1: Clone the repo

```bash
git clone https://github.com/TheRealMarvin/GOAP.git
cd GOAP
```

### Step 2: Install the (minimal) requirements
Because we believe in simplicity, this should be a breeze. You can run the whole thing with default Python—no exotic libraries, no 42-step installation guides, just the basics!

### Step 3: Run the show!
```bash
python main_cook.py
```
To start the magic, you have two options: either the Cooking Task or the Fighting Task.

#### Cooking Task
```bash
python main_cook.py --mode plan --heuristic enabled
```
Parameters:
- mode: Choose between plan (to generate and display the plan) and execute (to execute the plan).
- heuristic: enabled or disabled to choose whether to use the heuristic in planning.

#### Fighting Task
```bash
python main_fight.py --mode plan --heuristic enabled
```
Parameters:
- mode: Similar to the cooking task, choose between plan and execute.
- heuristic: enabled or disabled for heuristic planning.
Sit back, relax, and enjoy as your NPCs plan their next move in a world filled with virtual dilemmas and questionable choices. Who knows? Maybe they’ll even succeed!

---

## 🤔 NAQ (Never Asked Questions)

### ❓ Can I use your code in my project?
**Answer:** Yes, as long as you’re respecting the license. However, keep in mind that this project is really just an exploration of GOAP and a test of its limits. The implementation is pretty barebones, and you might need more features in your project. Also, the code isn't exactly what you'd call "clean," but it works for my needs (aka duct-tape level functionality).

### ❓ Do you support interrupting plans?
**Answer:** Yes! There are two ways to interrupt a plan. First, there’s an event handler that can stop an action before it’s complete. In this case, the state doesn't update, and we replan from where the action started (not the most perfect behavior, but hey, it’s something!). The second way is that we check preconditions before executing an action. If they’re not valid, we ask for replanning like an over-caffeinated project manager.

### ❓ Your code is missing so and so…
**Answer:** You’re probably right. 😅

### ❓ Hey, I saw your code and I want to use it in my game of Go, can you help me?
**Answer:** Oh, I hate to break it to you, but this probably isn’t the right approach to solve your Go game problem. Why? Well, GOAP is more about planning in a fairly static environment, not dealing with the deep complexities of ancient board games. It doesn't handle turn-based planning or high-dimensional strategy all that well. You might want to try something like Monte Carlo Tree Search or even Minimax instead!

*Also, a side note: GOAP isn't great for situations where there's an agent actively opposing you, especially when it requires long-term planning. It tends to get... a bit confused when someone’s messing up its plans!*


---

## 🤖 Acknowledgements

Some of the text in this README and portions of the example code were enhanced with the help of **ChatGPT**, which was used to make everything sound way cooler and help clarify some of the GOAP implementation details. 🎉
