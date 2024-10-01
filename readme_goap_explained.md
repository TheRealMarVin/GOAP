# 🧠 GOAP Explained – Under the Hood (aka “What’s Really Happening Here?”)

## 🎬 What Even Is GOAP?
GOAP (Goal-Oriented Action Planning) is basically how we get our little NPC buddies to stop running around like headless chickens and start making decisions like they know what they’re doing. It’s an AI technique that lets them figure out how to achieve goals all on their own, even when the world is throwing them curveballs.

---

## 🛠️ The Big Players in GOAP (Meet the Cast)

### 1. **Actions – The To-Do List**
Actions are the basic tasks our agent can perform. Think of them as the NPC’s “to-do list” items, but way more important than “buy milk.” Each action has:
- **Preconditions**: The stuff that needs to be true before the action can happen. Example: You need firewood before you can "start a fire."
- **Effects**: The changes this action will make. Example: After starting the fire, you now have a "fire going."
- **Cost**: How hard, time-consuming, or resource-draining the action is. Like choosing between jogging or ordering a pizza.
- **Duration**: How long it takes to pull off this action.

So, our `Action` class is basically a manager keeping track of these details and checking if the action is even possible before our NPC goes charging in.

### 2. **States – The World as We Know It**
A **State** is the current snapshot of the world. It’s a collection of facts about the agent’s reality. For example, `{"wood_collected": 1, "fire_started": 0}` means the agent has some wood but hasn’t started a fire yet.

The agent’s goal? Change this state to match what they want. Simple, right?

### 3. **Goals – What We’re Trying to Achieve**
Goals are the things the agent wants to achieve, like “cook a meal” or “defeat all enemies” (because, you know, NPC life). Each goal is just a state we want to reach. For example, `{"meal_cooked": 1}` is a goal in the cooking task. This is the dream the agent is chasing.

### 4. **The GOAP Planner – The Mastermind**
The **GOAP Planner** is the brains of the operation. It’s the one responsible for figuring out the “how” in "How do I reach my goal?" It takes:
- The **Start State** (Where we are now)
- The **Goal State** (Where we want to be)
- All the **Actions** (What we can do)

Then, it generates a **plan**—a sequence of actions to get from point A to point B, like an over-caffeinated GPS.

### 5. **The Agent – Our Hero**
The **Agent** is the one doing all the work. It takes the plan from the planner, executes it, and occasionally panics when things don’t go according to plan. The `Agent` class knows how to handle events, replan if necessary, and keeps things running smoothly (mostly).

### 6. **Event Manager – The Plot Twist Generator**
The **Event Manager** is like life throwing you a surprise party when you’re just trying to get some work done. It handles all those unexpected events that can mess up the agent’s plan and tells the agent, “Hey, time to replan!” 

## 🔍 The Big Steps of GOAP (How It All Works, Step-by-Step)

### 1. **Step One: Defining Actions**
First, we tell the agent what it can do. This is like giving them a list of all possible actions, with the preconditions they need and the effects they’ll have. Example: "Gather wood," "Cook meal," etc.

```python
gather_wood = Action(
    name="Gather Wood",
    preconditions={"has_axe": 1},
    effects={"wood_collected": 1},
    duration=5,
    cost=2
)
```

### 2. Step Two: The Agent Gets a Brain (Setting Up the Planner)
Next, we give our agent some smarts by setting up the GOAP Planner with all available actions and maybe a handy heuristic to help them plan more efficiently.

```python

planner = GOAPPlanner(actions, heuristic=fight_heuristic)
agent = Agent(actions, planner, event_manager, verbose=True)
```

### 3. Step Three: Planning Time!
The GOAP Planner looks at the agent’s start state, goal state, and context (extra info), then works out a plan using its favorite method—A* search (because A+ wasn’t good enough). It figures out which actions get the agent to its goal most efficiently.


### 4. **Step Four: The Agent Does Stuff (Executing the Plan)**
Now it’s time for the agent to roll up their sleeves and get to work. They start executing the plan step-by-step:
- Check if each action can still be done (preconditions met? ✔️).
- Do the action, update the state, feel accomplished.
- If something goes wrong, start sweating, then replan.

### 5. **Step Five: When Things Go Sideways (Replanning)**
Let’s be real: life happens. Sometimes, things don’t go according to plan (an enemy moves, or you drop your firewood). When that happens, the agent’s event handler steps in and says, “Uh-oh, time to replan!” The GOAP Planner generates a new plan based on the latest state of the world.

### 6. **Step Six: Mission Accomplished!**
The agent keeps going until they reach their goal. Then they pat themselves on the back (metaphorically, of course) for a job well done.

---

## 🧠 How Heuristics Work (a.k.a., the Agent’s Secret Sauce)
A heuristic is like a cheat sheet that helps the GOAP Planner find the best path faster. It’s an estimation of how much it’ll cost to reach the goal from where we are now. The planner uses it to avoid getting lost and wandering around like an NPC with no quest. Example: For a fighting task, the heuristic might be “distance to each enemy + their remaining health.”

---

## ⚙️ How It All Comes Together
Here’s the TL;DR of how GOAP fits together in your code:

1. **Initialization**: Create the agent, actions, planner, and event manager.
2. **Planning**: The planner generates an action sequence to reach the goal.
3. **Execution**: The agent executes actions, updates the state, and maybe panics if things go wrong.
4. **Replanning**: The agent reacts to unexpected events and replans if needed.
5. **Completion**: The agent reaches its goal, and everyone lives happily ever after (or until the next task).

---

## 🚀 Summary (The Short and Sweet Version)
GOAP is like giving your NPCs a bit of a brain. It lets them figure out how to achieve goals even when the world is throwing obstacles their way. They define actions, plan a path to their goals, adapt to changes, and feel like little geniuses—well, until they mess up and need to replan, but that’s just part of the journey!
