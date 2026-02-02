# 🚗 Rush Hour Puzzle Solver using BFS and A* (Python)

## 📌 Project Overview
This project models and solves the **Rush Hour puzzle**, a sliding block game where the objective is to move the red car out of a traffic jam and reach the exit of the board.

The puzzle is solved automatically using **Artificial Intelligence search algorithms**, specifically **Breadth-First Search (BFS)** and **A* search**.

This project was developed as part of the **Problem Solving course (Master 1 – Visual Computing)**.

---

## 🧠 Problem Description
The Rush Hour puzzle consists of vehicles placed on a grid board.

Each vehicle:
- Has an ID,
- Has a position,
- Is oriented horizontally or vertically,
- Has a length (2 or 3 cells).

Vehicles can only move in their orientation direction, and movement is blocked by other vehicles or walls.

The goal is to move the red car (`X`) to the exit on the right side of the board.

---

## ⚙️ Implemented Components

### State Modeling
The puzzle state includes:
- Board dimensions
- Vehicle list
- Walls (if present)
- Board representation

Main functions implemented:
- Vehicle loading from configuration files
- Board generation
- Goal state checking
- Successor generation

---

### Node Modeling
Each node in the search tree contains:
- Current puzzle state
- Parent node
- Applied action
- Path cost
- Evaluation function for A*

Functions include:
- Path reconstruction
- Solution extraction
- Evaluation computation

---

## 🔍 Search Algorithms

### Breadth-First Search (BFS)
- Explores states level by level.
- Guarantees shortest solution.
- May consume large memory.

### A* Search
Uses heuristics to guide search:

- **h1:** Distance from red car to exit.
- **h2:** Distance plus number of blocking vehicles.
- **h3:** Custom heuristic to improve search efficiency.

---

## 🎮 Game Interface
A graphical interface built with **Pygame** allows:
- Visualization of puzzle states,
- Simulation of the solution,
- Display of search cost and steps.

---

## 🛠 Technologies Used
- Python
- BFS and A* algorithms
- Pygame for visualization
- State-space search modeling

---



