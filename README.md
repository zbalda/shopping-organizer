# Call of 2D Zombies
### A 2D Zombie Survival Game

Call of 2D Zombies is a two-dimensional zombie survival game with an overhead viewpoint. The player can move a character around the screen with keyboard input and aim a weapon with the mouse. Left clicking will fire a weapon in the direction of the mouse pointer. Zombies (squares) come in waves that increase in difficulty. The player has limited health, and each contact with a zombie decreases that health. The player’s goal is to shoot and kill the zombies, surviving for as long as possible.

Framework used: http://www.gametutorial.net/article/Java-game-framework
The framework creates the game window, sets up the method to draw to the window, tracks user input, and sets up the main game loop.


## Classes
1.	Window
..1.  Creates a full screen window and places an instance of Framework on it
2.	Canvas
..* Canvas extends JPanel
..1.  Listens for and tracks keyboard and mouse events
..2.  Handles graphics and drawing methods
3.	Framework
..1.  Framework extends Canvas
..2.  Is the main game loop that updates and draws the Game
..3.  Has an instance of the Game class
..4.  Handles a few mouse events
4.	Game
..1.  Has all game objects
..2.  Tracks game statistics
..3.  Handles updating game objects, components, and displays
..4.	Handles collision detection
..5.  Handles drawing game objects and display
..6.  Handles all other gameplay


## Features
-	Menu, cursor, and game map - images and displays
-	A player that moves on an 2D plane based on user input (position, velocity, and acceleration)
..* Collision detection with enemies
....* Player enemy collisions decrease player health
....* If player dies, game is over
..* Collision detection with walls
..*	Player bounces off the walls of the screen
-	A weapon for the player that can shoot bullets in the direction of the mouse pointer (when mouse is clicked, if enough time has passed since the last click)
..*	The weapon fire speed increases as rounds go on
..* Collision detection between enemies and bullets
....*	Enemy bullet collisions subtract health from the enemy, possibly remove that enemy (if enemy dies), and remove the bullet
..* Collision detection between bullets and walls
....*	Bullets that go out of screen are removed
-	Enemy waves
..*	Enemies come in waves, increasing in difficulty
....*	More enemies spawn per wave as wave number increases
....*	Enemy health increases and wave number increases
....*	Player gets more ammo at the start of each wave
....*	Enemies spawn from random positions outside of the screen
-	Enemy AI
..*	Enemies follow the player, some more delayed than others
..*	Three types of enemies
..*	Regular enemies – regular size, speed, and health
..*	Smart enemies – smaller, faster, but have less health
..*	Large enemies – larger, slower, and more delayed, but have more health
..* Game statistics
....*	Wave, kills, ammo, score, health
....*	In game, pressing F1 toggles display of:
..*	Screen display size
..*	Current player position and velocity
..*	Number of spawned enemies and number of enemies to be spawned


## Algorithm
Run Process (from start)
•	Program is started
•	Main is called in Window, creates a window
•	Window creates a Framework (extends Canvas) and adds it to its content pane
•	Constructor of Framework calls the constructor of Canvas, sets the state to VISUALIZING, creates a thread for the game loop, and calls the GameLoop() of Framework
•	GameLoop() on state VISUALIZING sets the frame height and width, sets the state to STARTING, and calls repaint()
•	Repaint() calls Draw(), which doesn’t draw anything in this state (VISUALIZING)
•	GameLoop() on state STARTING calls Initialize() and LoadContent(), then sets the state to MAIN_MENU, and calls repaint()
•	Initialize sets the font for the menu
•	Load content loads images, sound, etc. for the menu
•	Repaint() (Draw()) in this state (STARTING) doesn't draw anything
•	GameLoop() on state MAIN_MENU calls repaint()
•	If ESC is pressed, the game is exited
•	If left mouse is clicked, newGame() is called
•	Repaint() (Draw()) in this state (MAIN_MENU) draws the menu text and images
•	NewGame() creates a new Game()
•	Game() constructor sets the game state to GAME_CONTENT_LOADING
•	A new thread is created for the initialization of the Game class
•	In this thread, Initialize() and LoadContent() of the Game class are called, and afterward the game mode is set to PLAYING
	Initialize sets the font, variables, array lists, etc. for the game
	LoadContent loads images, sound, etc. for the game
•	While the game is being initialized on its own thread, the game loop of Framework (on GAME_CONTENT_LOADING) draws a "Game is Loading" screen
•	GameLoop() now on PLAYING runs the regular game loop
•	For each loop (for more detail, see game loop descriptions)
	Update game
	Collision detection
	Draw
•	When Player dies, the state is set to GAMEOVER
•	GAMEOVER in GameLoop() does nothing
•	GAMEOVER in Draw()
•	We draw the game over screen with "Game Over", game statistics (game.DrawStatistics(g2d, gameTime)), and "Enter to restart or ESC to exit"
•	If Enter is pressed, restartGame() of framework is called
•	RestartGame() resets the game time, calls game.RestartGame(), and sets the state to PLAYING
•	ESC closes the window


## Game Loop
•	UpdateGame(long, point): void
•	limitMousePosition
•	UpdatePlayer
•	Update position
	Did player hit off wall
•	Update posHist
•	Update weapon
	Update weapon level
	Is player shooting
	Update bullet positions
•	Bullets off screen are removed
•	Done either here or in collision detection
•	UpdateWaves(long): void
•	UpdateWaves(): void
	Spawning, etc.
•	UpdateEnemies(): void
	Updates each enemies position and calculates new direction for each (accesses player position history - may need to be passed player history)
•	Collision Detection
•	Check collision between bullets and enemies
•	If there is a collision, remove bullet, update enemy health, update enemy alive status, and possibly remove enemy
•	Gets players position and checks it with position of each enemy
•	If player collides with enemy, update player health, update player alive status
•	Bullets off screen are removed
•	Draw
•	Draw(Graphics2D, Point, long): void
•	Draw background, player, bullets, enemies
•	DrawStatistics(Graphics2D, long): void
•	DrawMouse(Graphics2D, Point): void


## Class Descriptions

### Window
-	Window extends JFrame
-	Main method is in Window
-	Constructor
o	Sets title
o	Sets to undecorated and full screen
o	Sets default close operation to exit_on_close
o	Sets the content pane of the window to an instance of Framework
	Framework extends Canvas, which extends JPanel
o	Sets window visibility to true

### Canvas
-	Canvas extends JPanel and implements KeyListener and MouseListener
o	For drawing and getting user input
-	Variables (two Boolean arrays)
o	One for tracking the current state of the keyboard (keyBoardState[525])
	If a key is pressed, its corresponding index position in the keyboard array is set to true
	If a key is released, its corresponding index position in the keyboard is set to false
o	One for tracking the current state of the mouse (mouseState[3])
	Same for mouse
-	Constructor
o	Sets buffer method, focusable, and background color
o	Sets cursor to blank (custom cursor will be added later)
o	Adds mouse and key listeners
-	Methods
o	Canvas has methods for returning the Boolean value at an index position of the mouse or keyboard array
	Public static Boolean keyboardKeyState(int key)
	Public static Boolean mouseButtonState(int button)
o	Canvas also has methods for drawing Graphics to the panel

### Framework
-	Framework extends Canvas
-	Framework is essentially the game loop
o	Updates 60 times per second
o	Draws at 60 FPS
-	Variables
o	frameWidth and frameHeight (in pixels of screen) calculated in game state visualizing
o	secInNanoSec – 1 second in nanoseconds (used for conversions)
o	millisecInNanosec – 1 millisecond in nanoseconds (used for conversions)
o	GAME_FPS – how many times we update and draw per second
o	GAME_UPDATE_PERIOD – used to calculate sleep time so game loop meets FPS
o	Enumeration GameState - all of the possible game states
o	GameState gameState – current game state
o	gameTime – elapsed time since start of game
o	lastTime – used for calculating elapsed time
o	Game game – actual game, game objects, etc.
o	Fonts and an image for the menu
-	Constructor
o	Calls constructor of parent class
o	Sets game state to VISUALIZING
o	Creates a separate thread for the game loop
o	Calls the game loop
	Game loop in state VISUALIZING gets the frameWidth and frameHeight
	When that is done, the state is set to STARTING, which calls Initialize() and LoadContent()
-	Methods
o	Initialize - sets font types for menu
o	LoadContent – loads the menu background image
o	GameLoop (ran ~60 times per second)
	Game states (enumeration)
•	PLAYING
o	Calculates game time
o	Calls game.UpdateGame(gameTime, mousePosition())
o	Updates lastTime to current System time (in nanos)
•	GAMEOVER
o	Does nothing (for updating)
•	MAIN_MENU
o	Does nothing (for updating)
•	OPTIONS
o	Does nothing
•	GAME_CONTENT_LOADING
o	Does noting (for updating)
•	STARTING
o	Calls Initialize(), which sets font type for menu
o	Calls LoadContent(), which loads the menu background image
o	Sets the game state to STARTING
•	VISUALIZING
o	Gets screen resolution to set frameWidth and frameHeight
o	Sets state to STARTING
	Calls Draw
o	Draw (Graphics2d g2d) (called from GameLoop ~60 times per second)
	Game states (enumeration)
•	PLAYING
o	Calls game.Draw(g2d, mousePosition(), gameTime)
•	GAMEOVER
o	Calls game.DrawGameOver(g2d)
	Which draws “GAME OVER” with game stats
•	MAIN_MENU
o	Draws main menu background image, game title, and game instructions
•	OPTIONS
o	Does nothing
•	GAME_CONTENT_LOADING
o	Draws a white screen with “Game is Loading”
o	newGame
	Sets the game time to 0, sets last time to current System time, and creates a new Game object (which restarts everything)
o	restartGame
	Sets gameTime to 0, last time to current System time, calls game.RestartGame(), and sets the game mode to PLAYING
o	mousePosition
	Returns mouse position, unless position is null (off screen), in which case it returns (0,0)
o	keyReleasedFramework(keyEvent e)
	Game states (enumeration)
•	GAMEOVER
o	ESC closes the program
o	ENTER restarts the game
•	PLAYING
o	F1 toggles the game stats (position, velocity, etc.)
•	MAIN_MENU
o	ESC closes the program
o	mouseClicked(mouseEvent e)
	Game states (enumeration)
•	MAIN_MENU
o	Mouse BUTTON1 creates a new game

### Game
-	Variables
o	Player player
	player handles player health, kills, position history, acceleration from user input, updating player position, drawing player, updating and drawing weapons and bullets, etc.
o	Waves waves
	handles generating new waves, tracking wave number, spawning enemies, updating enemies, drawing enemies, etc.
o	Score – earned from killing enemies and surviving waves
o	backgroundImg – the game map grid image
o	mouseCursorImg – crosshair image
o	Fonts – for on screen display
o	Static Boolean displayF1stats for whether F1 stats should be drawn
-	Constructor
o	Creates a separate thread for Initializing() and LoadContent() to be called
	Initialize()
•	Creates a new Player
•	Creates a new Waves
•	Sets the score to 0
•	Sets font types
•	Sets displayF1stats to false
	LoadContent
•	Loads game map grid image
•	Loads crosshair image
•	Calculates center of mouse crosshair image
	Sets the game state to PLAYING
-	Methods
o	RestartGame
	Creates a new player
	Creates a new waves
	Sets score to 0
o	UpdateGame(gameTime, mousePosition)
	If play is alive
•	Update player
•	Update player weapon, passing gameTime and mousePosition
•	Update waves, passing gameTime
•	Update enemies, passing player position history
•	Run collision detection
	If player is dead
•	Set game state to GAMEOVER
o	Collision Detection
	For each enemy, check if any bullets collide (if rectangles intersect)
•	If bullet does collide, subtract health from enemy, getAliveStatus to possibly remove enemy, and remove bullet
	For each enemy, check if enemy collides with player (if rectangles intersect)
•	If enemy collides with player, subtract health from player, getAliveStatus from player and possible set game state to GAMEOVER
o	Draw(Graphics2D g2d, mousePosition, gameTime)
	If player is alive
•	Draw background image
•	Draw bullets
•	Draw enemies
•	Draw player
•	Call DrawGameStatistics(g2d, gameTime)
•	Call drawMouseCursor(g2d, mousePosition)
o	DrawGameStatistics(Graphics g2d, gameTime)
	If displayF1stats == true, draw
•	Frame size, x and y velocity, x and y position, total enemies, and total enemies to be spawned
	Draw
•	Wave number, total kills, ammo, score, and health
o	DrawMouseCursor(Graphics2D g2d, mousePosition)
	Draw mouse cursor with center of cursor image at mouse point
o	DrawGameOver(Graphics2D g2d)
	Draw (game objects are drawn but not updated – appear frozen)
•	Background image
•	Bullets
•	Enemies
•	Player
•	Game title and “GAME OVER”
•	Game stats – wave, kills, score

### Player
-	Variables
o	HealthAtStart – player has 100 health at the beginning of each game
o	Health – current health, starts at 100
o	Boolean alive – updated during collision detection if player collides with enemy
o	totalKills – updated during collision detection if enemy dies
o	x and y position, and x and y velocity – changing variables
o	x and y acceleration and deceleration – constant
o	player size – x any y length of player rectangle
o	weapon – player weapon, which fires, updates, and draws bullets
-	Constructor
o	Set x and y position to the passed x and y
o	Set health to 100
o	Set kills to 0
o	Set player size to 50
o	Set acceleration and deceleration to .2
o	Initialize all other variables
-	Update
o	Call updateVelocity()
o	Call updatePosition()
o	Call updatePositionHistory()
-	updateVelocity
o	IMPORTANT
	dx positive moves to the right
	dx negative moves to the left
	dy positive moves down
	dy negative moves up
o	Key input acceleration and deceleration
	If D key is pressed, add ddxMove to dx (accelerate to the right)
	If A key is pressed, subtract ddxMove from dx (accelerate to the left)
•	If neither A nor D is pressed, decelerate player dx
	If magnitude of dx is greater than 6, set to 6 (max velocity)
	^ same for DY with W and S keys
o	If bullets hits off of any walls, inverse its velocity for whatever wall it hit
-	updatePosition
o	Add dx to x and dy to y
-	updatePositionHistory
o	Add current position to end of position history linked list
o	If linked list is greater than 60, remove that first (oldest) item
-	UpdateWeapon
o	If mouse is pressed, call weapon.tryShoot, which shoots the weapon if enough time has passed since the last fired bullet
o	Call weapon.updateBullets, which moves each bullet
o	Call weapon.clampBullets, which removes any bullets that go off screen
-	tryDamagePlayer
o	If enough time has passed since player was last damaged, damage again
-	getAliveStatus
o	Update Boolean alive based on player health and return status
-	getPositionHist
o	returns linked list of player history
-	removeBullets
o	Gets linked list of Booleans from game, and sends them to weapon for which bullets should be removed
-	drawBullets
o	Draws each bullet
-	drawPlayer
o	Draws the player
-	getBounds
o	returns player rectangle
Position History
-	Variables
o	x and y for position
o	dx and dy for velocity
-	Constructor
o	Sets x, y, dx, dy (player position when set)
-	Methods
o	Getters and setters

### Weapon
-	Variables
o	ammo – ammo count
o	time of last created bullet and time between bullets – for handling fire rate
o	array list of bullets – current bullets being shot
-	Constructor
o	Sets ammo to 10
o	Puts a half second delay between bullet firing
o	Initializes the array of bullets
-	Methods
o	tryShoot
	fires a bullet if enough time has passed
o	update bullets
	calls update on each bullet in the array list
o	clamp bullets
	removes any bullets that go out of the screen
o	remove bullets
	gets passed an array list of bullets to be removed (from collision detection), and removes those bullets
o	update weapon level
	called at the start of each new wave
	increases fire rate
o	drawBullets
	draws each bullet
o	getBulletRectangles
	returns an array list of bullet rectangles for collision detection in Game
o	getBulletCount
	returns total number of bullets (not ammo count)

### Bullet
-	Variables
o	Position x and y, velocity dx and dy
o	Speed and damage
o	size
-	Constructor
o	Sets x and y (which, when created, is the players position)
o	Sets dx and dy, which are later changed
o	Sets the bullet size
o	Calls setVelocity and passed the mouse position
-	Methods
o	updateBullets
	adds dx to x and dy to y
o	draw
	draws the bullet
o	setVelocity
	based on player position when bullet is fired and mouse position when bullet is fired, a the dx and dy are calculated to create a velocity vector that will follow the mouse – i.e. the bullet x and y velocity is set to fire the mouse position
o	getters

### Waves
-	Variables
o	Wave number, for tracking wave number
o	Amount of each enemy to be spawned – calculated at beginning of each round
o	Enemy health levels – calculated at beginning of each round, increase each round
o	Ammo to add – calculated at beginning of each round, added to weapon ammo count
o	Array lists of enemies
o	Time of last created enemy (for each enemy type) – used for spawning
o	Time between enemy spawns (for each enemy type) – used for spawning
-	Constructor
o	Initializes variables
o	Initializes enemy array lists
o	Sets state to CALCULATING NEW WAVE
-	Methods
o	UpdateWaves(gameTime)
	Game States
•	CALCULATING_NEW_WAVE
o	Increments wave number
o	Calculates enemies to be spawned (for each enemy type)
o	Increases enemy health (for each enemy type)
o	Calculates and adds ammo to weapon
o	Updates weapon fire rate based on wave number
o	Sets state to DELAY
•	DELAY
o	Waits 8 seconds to start spawning enemies
o	Sets state to spawning
•	SPAWNING
o	Tries to spawn each type of enemy
	Enemies spawn if enough time has passed
o	Calculates total enemies to be spawned
	If there are no enemies to be spawned, state is set to FINISHING
•	FINISHING
o	Calculates total enemies left
	When there are no enemies left
•	Add to game score
•	Set state to CALCULATING_NEW_WAVE
o	tryEnemySpawn – for each type of enemy
	If enough time has passed to spawn an enemy, and enemy is spawned at a random location right outside of the screen
o	updateEnemies
	calls calculate new direction (follow player) on all enemies
	calls update on all enemies
o	damageEnemies
	Collision detection done in Game returns a Boolean linked list of what enemies to damage in the array of enemies (for each enemy type)
•	This enemies are then damaged (health taken away)
•	We call get alive status, and if the enemy health is < 0
o	Alive status is set to false
o	Game score is increased
o	Total kills gets +1
o	DrawEnemies
	Draws all enemies (of each type)
o	getEnemyRectangles
	returns an array list of rectangles of all enemies for collision detection to be done in Game

### Enemy
-	Variables
o	Position x and y
o	Velocity dx an dy
o	Speed (for calculating dx and dy)
o	size
-	Initializer
o	Sets health to passed value, passed from waves when the enemy is spawned
	Enemy health increases as rounds go on
o	x set to passed x, y set to passed y
o	dx set to passed dx, dy set to passed dy
-	Methods
o	updatePosition
	adds dx to x, and dy to y
o	getters for x and y
o	damage
	subtracts the passed amount from health
o	getAliveStatus
	updates enemy alive status (true == alive, false == dead) based on enemy health
	returns that status
o	getBounds
	returns enemy rectangle for collision detection in Game
BasicEnemy, SmartEnemy, LargeEnemy
-	Variables
o	None
-	Constructor
o	Calls Enemy constructor
o	Sets speed and size
-	Methods
o	calculateNewDirection – called at 60 times per second, for each game loop
	gets passed the position history of the player
	calculates dx and dy for enemy, such that enemy follows player
o	draw
	draws the enemy









## Data Design

As seen from the class descriptions, this program is entirely object oriented. The game loop (Framework) has an instance of Game, which gets updated, checked for collisions, and drawn for each loop. The game holds all objects and all data of the game, which include:

-	Player // player can update and draw itself and call update and draw on weapon
o	Weapon // weapon can update itself and call update and draw on bullets
	Bullet // bullets can update and draw itself
-	Waves // waves can update itself and call update on enemies
	Enemies // enemies can update and draw itself
-	Array lists are used for just about everything
o	Enemies, bullets, player position history, etc.
-	Integers are used to keep track of game statistics
-	We create a Graphics2D g2d that we essentially pass around to the player, enemies, statistics, etc. to draw everything on it then put it on the screen (for each frame)
-	Images are used for the menu, the in game background, and crosshair
