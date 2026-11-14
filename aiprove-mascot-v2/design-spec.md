# Pip v2 — GPT design specification (verbatim outputs, combined)

Source files in this workspace: mascot-v2-gpt-output.txt (design v1), mascot-v2-fix-output.txt (brim fix + first pose fixes), mascot-v2-fix2-output.txt (corrected sections 5 and 6). The SVGs were built from the v1 spec as corrected by the brim fix and fix2.

## 1. Design v1

## 1. CHARACTER

**Direction chosen: (A) Evolve Pip into a clearly stronger v2**, because the original character already combines the required newspaper and terminal ideas, while sharper geometry, stronger silhouette cues, and a more distinctive trophy-and-headline identity make Pip more memorable at small sizes.

**Name:** Pip v2, “The Circuit Courier.” Pip is a compact newsboy robot whose CRT head reads the arena, whose folded newspaper body carries the daily headline, and whose terminal-green face reacts to building, grading, and winning. The character wins through a single unmistakable silhouette: tilted newsboy cap, glowing pixel face, folded broadsheet torso, and a small green antenna tip. Pip feels like the cheerful field reporter and scorekeeper of an open bounty arena without adding any unprovided claims about AIProve.

**Personality:** alert, generous, victorious.

## 2. PALETTE (exact, final)

Use exactly these six colors across all character artwork:

- **Newsprint Cream — `#F3E7C8`**  
  Main CRT casing, folded newspaper torso, paper props, trophy highlight panels, desk papers, and ground-shadow-free negative space within paper objects.

- **Ink Black — `#171A1A`**  
  All exterior outlines, cap, screen, limbs, feet, newspaper print columns, keyboard keys, trophy outline, and pixel facial features when an unlit detail is required.

- **Terminal Green — `#64F38A`**  
  Antenna tip, eyes, smile, terminal strings, terminal-screen accents, small circuit marks, winner sparkles, and selected confetti.

- **Terminal Deep Green — `#1E6B4A`**  
  Secondary terminal-screen panel, keyboard base, antenna stem, and small dark-green newspaper registration marks. It must remain visibly darker than Terminal Green.

- **Press Gold — `#E0A83E`**  
  Trophy, cap button, winner badge accent, trophy sparkle centers, and one small newspaper seal shape. Use sparingly.

- **Press Red — `#C84B3A`**  
  A single cap ribbon stripe, selected paper scraps, and two champion confetti pieces. It is the only warm color besides Press Gold.

No transparency is used inside the character except the specified ground shadows and background marks. Do not introduce white, gray, blue, purple, or additional beige tones.

## 3. ANATOMY & PROPORTIONS

Use a 1200 × 1200 px canvas. In the neutral standing pose, Pip occupies approximately 430 px wide × 670 px tall, from the antenna tip at y=245 to the bottom of the feet at y=915. The character is centered on x=600. All exterior outlines use **Ink Black `#171A1A` with a consistent 14 px stroke, round joins, and round caps**. Internal newspaper rules and keyboard divisions use 5 px Ink Black strokes and are not silhouette outlines.

### Head

The head is a rounded CRT casing: a rounded rectangle **360 px wide × 270 px tall**, positioned at **x=420, y=280**, with **55 px corner radius**. Fill it Newsprint Cream. Outline it with 14 px Ink Black. The casing has a shallow lower bevel represented by a 5 px Ink Black horizontal rule from x=470 to x=730 at y=515. The head is the main visual anchor and remains the same size and position in every pose.

### Face/screen

The face screen is a rounded rectangle **304 px wide × 184 px tall**, positioned at **x=448, y=325**, with **24 px corner radius**. Fill it Ink Black and outline it with 14 px Ink Black, so the screen merges visually into a heavy dark frame. Leave at least 28 px of cream casing visible around the screen.

The face is constructed only from square pixel blocks in Terminal Green:

- Left eye: **24 × 24 px square** at x=505, y=370.
- Right eye: **24 × 24 px square** at x=671, y=370.
- Smile: seven **18 × 18 px squares** arranged as a pixel arc. Place blocks at `(526,426)`, `(544,444)`, `(562,462)`, `(580,462)`, `(598,462)`, `(616,444)`, and `(634,426)`. Add two 18 × 18 px blocks at `(544,462)` and `(652,444)` only if the expression needs a wider open smile; the standard neutral face uses the seven-block arc.
- Add two 12 × 12 px Terminal Green squares at x=478 and x=710, y=344 as screen-status pixels.

For the standard expression, use the seven-block smile. In the Champion pose, add the two optional lower-corner blocks to make the smile visibly wider. In the At Work pose, move the eyes down 8 px and use the same seven-block smile with the outermost two blocks omitted, creating a focused expression.

### Cap or headgear

The cap is a tilted newsboy cap in Ink Black, rotated **−10 degrees around x=600, y=300**. Its main crown is a flattened rounded dome path occupying **390 px wide × 112 px tall**, with the unrotated bounding box x=405, y=216, width 390, height 112. Use a 14 px Ink Black outline and Ink Black fill.

The brim is a flattened capsule-like path **170 px wide × 40 px tall**, centered at x=530, y=302 before rotation. Fill Ink Black and outline with 14 px Ink Black. The brim projects leftward beyond the head casing. The cap crown includes a 9 px Press Red stripe following the lower crown curve from x=465 to x=620 before rotation. Place a **22 × 22 px Press Gold square button**, rotated with the cap, at the crown’s upper center around x=600, y=238.

### Antenna

The antenna stem is a rounded rectangle **12 px wide × 52 px tall**, positioned at x=594, y=228, with a 6 px radius. Fill Terminal Deep Green and outline with 14 px Ink Black. It emerges from behind the cap button and leans 4 degrees to the right.

The antenna tip is a Terminal Green circle with **22 px diameter**, centered at x=610, y=212, outlined in 14 px Ink Black. The visible green interior is approximately 8 px across after the outline. This bright dot is the primary recognition cue at 64 px.

### Torso/body

The torso is a folded broadsheet newspaper represented by a rounded rectangle **330 px wide × 232 px tall**, positioned at **x=435, y=548**, with **22 px corner radius**. Fill Newsprint Cream and outline with 14 px Ink Black.

The top edge is tucked behind the head’s lower edge by 8 px. Add a folded-paper triangular corner on the lower right: a Newsprint Cream triangle with points `(702,754)`, `(765,754)`, `(765,691)`, outlined with 14 px Ink Black. Its fold line is a 5 px Ink Black diagonal from `(702,754)` to `(765,691)`.

The exact headline is **`DAILY // CIRCUIT`**, set in a bold condensed sans-serif, all caps, Ink Black, **30 px**, horizontally centered at x=600, with its text baseline at y=596. Use `font-family="DejaVu Sans Condensed, Arial Narrow, sans-serif"`, `font-weight="700"`, and `letter-spacing="1 px"`.

Below the headline, draw three newspaper columns with 5 px Ink Black rules:

- Column rule 1: x=493, from y=622 to y=720.
- Column rule 2: x=600, from y=622 to y=720.
- Column rule 3: x=707, from y=622 to y=704.

Add short horizontal print lines, each 5 px thick, in Ink Black. In column one use segments from x=462–485, 498–570, 462–535, 542–570, and 462–570 at y=638, 655, 678, 696, and 716. In column two use segments from x=615–682, 615–690, 615–665, and 615–690 at y=638, 655, 678, and 699. In column three use segments from x=722–750, 722–750, and 722–742 at y=638, 655, and 678. These are abstract print rules, not readable words.

Place a Press Gold circular seal, **28 px diameter**, centered at x=731, y=729, outlined in 5 px Ink Black. It contains one Terminal Green 8 × 8 px square. This seal is a graphic mark, not text.

### Arms

In the neutral standing pose, each arm is a dark robot limb built from two rounded capsule segments.

The left upper arm is a rounded rectangle **22 × 105 px**, radius 11, from centerline `(426,588)` to `(392,673)`. The left forearm is a rounded rectangle **20 × 92 px**, radius 10, from centerline `(392,673)` to `(370,748)`. Fill Ink Black with 14 px Ink Black outline.

The right upper arm is a rounded rectangle **22 × 105 px**, radius 11, from centerline `(774,588)` to `(808,673)`. The right forearm is a rounded rectangle **20 × 92 px**, radius 10, from `(808,673)` to `(830,748)`. Fill Ink Black with 14 px Ink Black outline.

For posed arms, retain these segment widths and lengths, changing only their rotation and centerline positions. No arm may become thicker than 30 px including its outline.

### Hands

Each hand is a simple four-finger robot mitten: a rounded rectangle **38 px wide × 44 px tall**, with **16 px corner radius**, filled Newsprint Cream and outlined in 14 px Ink Black. The neutral left hand is centered at `(370,770)` and the neutral right hand at `(830,770)`. Fingers are implied by three 5 px Ink Black vertical grooves, each 7 px long, placed across the lower half of the hand. In waving and trophy poses, rotate the hand with the forearm.

### Legs

Two legs descend from behind the newspaper body. Each is a rounded rectangle **28 px wide × 118 px tall**, radius 14, filled Ink Black and outlined in 14 px Ink Black.

- Left leg: centerline from `(535,775)` to `(535,880)`.
- Right leg: centerline from `(665,775)` to `(665,880)`.

Leave a 102 px gap between their centerlines. The legs must remain simple and visibly separate at badge scale.

### Feet

Each foot is a horizontal rounded rectangle **82 px wide × 38 px tall**, with **18 px corner radius**, filled Ink Black and outlined in 14 px Ink Black.

- Left foot bounding box: x=492, y=872, width 82, height 38.
- Right foot bounding box: x=626, y=872, width 82, height 38.

The toes point outward by 8 degrees: rotate the left foot −8 degrees and the right foot +8 degrees around their centers.

### Signature details

1. **Green antenna bead:** the small Terminal Green circle above the cap remains visible in every pose and provides a one-pixel-bright signal at small sizes.
2. **Split cap stripe:** the Press Red stripe runs only along the lower left half of the cap, making the tilted cap recognizable without competing with the face.
3. **Gold circuit seal:** the Press Gold circular seal with a single green square sits on the lower-right newspaper fold and becomes Pip’s chest emblem.
4. **Folded lower-right corner:** the triangular newspaper fold produces a distinctive angular notch in the otherwise rectangular body silhouette.

## 4. POSE 1 — “WELCOME” (board header, onboarding)

Use the same 1200 × 1200 canvas and the same head, cap, antenna, torso, legs, and feet coordinates defined above. Pip stands centered, with the feet at y=910. Add one soft ground shadow ellipse behind the feet: **260 px wide × 28 px tall**, centered at `(600,925)`, fill Ink Black at **12% opacity**, with no outline.

Pip’s head tilts **−4 degrees around `(600,420)`**, in addition to the cap’s fixed −10-degree tilt. Keep the face at its standard seven-block smile. The screen eyes remain at their standard positions relative to the screen.

Pip’s left arm, on the viewer’s right, waves. Use an upper-arm capsule **22 × 105 px** centered from `(766,590)` to `(808,514)`, rotated to follow that line. Use a forearm capsule **20 × 92 px** centered from `(808,514)` to `(834,430)`. The left hand is centered at `(840,398)`, rotated **−12 degrees**, with the palm facing the viewer. Add three 5 × 18 px Ink Black finger grooves at the hand’s upper edge. The hand is open and welcoming.

Pip’s right arm, on the viewer’s left, bends across the lower torso. Use an upper-arm capsule from `(432,592)` to `(394,650)` and a forearm capsule from `(394,650)` to `(345,690)`. The hand is centered at `(322,704)`. It holds a rolled newspaper: a Newsprint Cream rounded rectangle **42 px wide × 170 px tall**, radius 21, tilted **−18 degrees**, centered at `(280,660)`, outlined with 14 px Ink Black. Add three 5 px Ink Black horizontal print rules at y=615, 651, and 688 within the roll, following its rotation. Cap both ends with 14 px Ink Black curved lines.

Add minimal background marks, all behind Pip:

- Three Terminal Green 12 × 12 px squares at `(190,330)`, `(965,380)`, and `(1000,700)`.
- Two Newsprint Cream paper scraps outlined in Ink Black, each 34 × 22 px: one rotated −18 degrees at `(205,760)`, one rotated +14 degrees at `(978,550)`.
- Four Ink Black halftone dots, each 10 px diameter at 20% opacity, centered at `(150,440)`, `(175,440)`, `(150,465)`, and `(175,465)`.

The feeling is an immediate, friendly invitation to enter the arena: Pip faces forward, waves high, and carries the newspaper as a welcoming dispatch.

## 5. POSE 2 — “CHAMPION” (winners, badges, results)

Keep the same head, cap, antenna, newspaper torso, legs, and feet dimensions and positions. Tilt the head **+3 degrees around `(600,420)`**. Use the expanded Champion smile: retain all seven standard smile blocks and add the two optional 18 × 18 px blocks at `(544,462)` and `(652,444)` relative to the screen, producing a broad open grin.

Both arms rise symmetrically to hold a trophy overhead.

The viewer-left arm uses an upper capsule from `(432,590)` to `(400,500)` and a forearm capsule from `(400,500)` to `(454,398)`. The hand center is `(475,378)`.

The viewer-right arm uses an upper capsule from `(768,590)` to `(800,500)` and a forearm capsule from `(800,500)` to `(746,398)`. The hand center is `(725,378)`.

The trophy is centered at x=600 and sits above the head, occupying **190 px wide × 160 px tall**, from y=180 to y=340. It has a Press Gold cup: a trapezoid with top edge from `(535,205)` to `(665,205)`, bottom edge from `(556,290)` to `(644,290)`, and side edges connecting those points. Fill Press Gold and outline with 14 px Ink Black. The upper rim is a rounded rectangle **142 × 24 px**, radius 12, positioned x=529, y=190, filled Press Gold and outlined in Ink Black.

The trophy handles are two Ink Black outlined Press Gold curved capsules, each **42 × 82 px**, 14 px stroke: left handle arcs from `(538,222)` toward `(500,268)` and back to `(550,286)`; right handle mirrors it from `(662,222)` toward `(700,268)` and back to `(650,286)`. The stem is a rounded rectangle **24 × 38 px**, radius 8, at x=588, y=289. The base is a rounded rectangle **108 × 24 px**, radius 10, at x=546, y=318. The trophy must overlap the raised hands slightly so the hands visibly support it.

Place eight confetti pieces behind Pip, each a 12 × 28 px rounded rectangle with 6 px radius and 14 px Ink Black outline:

- Terminal Green at center `(220,270)`, rotated −25 degrees.
- Press Gold at `(315,190)`, rotated +22 degrees.
- Press Red at `(910,250)`, rotated +28 degrees.
- Terminal Green at `(1000,330)`, rotated −18 degrees.
- Press Gold at `(185,555)`, rotated +32 degrees.
- Press Red at `(1015,650)`, rotated −30 degrees.
- Terminal Green at `(295,820)`, rotated −20 degrees.
- Press Gold at `(910,820)`, rotated +18 degrees.

Add four four-point sparkles, made from two intersecting Ink Black 6 px rounded bars with Terminal Green 14 × 14 px centers, at `(300,360)`, `(900,420)`, `(245,690)`, and `(965,720)`. Each sparkle has total width and height 42 px.

Add one soft ground shadow ellipse, 280 × 28 px, centered at `(600,925)`, Ink Black at 12% opacity.

The feeling is earned celebration: Pip is visibly supporting the trophy, smiling broadly, and surrounded by a controlled burst of pressroom confetti rather than generic party decoration.

## 6. POSE 3 — “AT WORK” (building, grading, launch thread)

Keep the same head, cap, antenna, torso, legs, and feet geometry. Pip remains standing behind a retro terminal desk, so the body is not resized or redesigned. Tilt the head **−2 degrees around `(600,420)`**. Use the focused expression: move both green eyes 8 px downward within the screen and omit the two outermost smile blocks, leaving the five central smile blocks from the standard seven-block arc.

The arms extend forward and down toward the keyboard.

The viewer-left arm uses an upper capsule from `(432,590)` to `(388,650)` and a forearm capsule from `(388,650)` to `(454,725)`. Its hand is centered at `(476,736)`, palm down.

The viewer-right arm uses an upper capsule from `(768,590)` to `(812,650)` and a forearm capsule from `(812,650)` to `(746,725)`. Its hand is centered at `(724,736)`, palm down. Hands use the standard Newsprint Cream mitten shape with three short Ink Black grooves facing the keyboard.

The desk is a flat retro terminal desk behind the hands and in front of the lower legs. Its top is a rounded rectangle **500 px wide × 48 px tall**, radius 18, at **x=350, y=742**, filled Newsprint Cream and outlined with 14 px Ink Black. The desk front is a rounded rectangle **450 px wide × 92 px tall**, radius 18, at x=375, y=786, filled Terminal Deep Green and outlined with 14 px Ink Black. Hide the lower halves of Pip’s legs behind the desk front.

Place a terminal monitor on the desk, centered at x=600. The monitor casing is a rounded rectangle **300 px wide × 190 px tall**, radius 28, at x=450, y=585, filled Newsprint Cream and outlined with 14 px Ink Black. This monitor sits in front of Pip’s torso but below the face, leaving the newspaper headline visible above it. Its screen is a rounded rectangle **252 px wide × 126 px tall**, radius 16, at x=474, y=617, filled Ink Black and outlined with 14 px Ink Black.

The monitor contains exactly two short terminal strings, each in Terminal Green, `font-family="DejaVu Sans Mono, Courier New, monospace"`, `font-weight="700"`, `font-size="18 px"`, with no additional text:

- `> GRADE: PASS` at x=492, baseline y=665.
- `> BUILD: LIVE` at x=492, baseline y=701.

The strings are aligned left and occupy no more than 220 px in width. Add three Terminal Green 8 × 8 px status squares at x=688, 704, and 720, y=628.

The keyboard is a rounded rectangle **220 px wide × 56 px tall**, radius 14, at x=490, y=735, filled Terminal Deep Green and outlined with 14 px Ink Black. Add two rows of 7 Ink Black key squares, each **16 × 12 px**, radius 3. Row one begins at x=510, y=750 with 26 px horizontal spacing; row two begins at x=523, y=772 with the same spacing. Keep the keys abstract and without text.

Place two stacked newspapers on the viewer-right side of the desk: each is a Newsprint Cream rounded rectangle **90 × 22 px**, radius 6, outlined in 8 px Ink Black. The lower paper is at x=802, y=716 and the upper paper at x=794, y=694, rotated +4 degrees. Add one 5 px Ink Black rule across each.

Place one loose paper sheet on the viewer-left side: a Newsprint Cream quadrilateral with points `(270,715)`, `(350,705)`, `(360,760)`, and `(280,770)`, outlined in 8 px Ink Black, rotated −5 degrees. Add three 5 px Ink Black print rules.

Add background elements behind Pip and the desk:

- One Terminal Deep Green horizontal line, 5 px wide and 150 px long, from x=160 to x=310 at y=310.
- One Ink Black horizontal line, 5 px wide and 110 px long, from x=890 to x=1000 at y=330.
- Three Terminal Green 10 × 10 px squares at `(220,370)`, `(990,470)`, and `(250,570)`.
- Two Press Red paper scraps, each 28 × 18 px with 8 px Ink Black outline, at `(930,590)` rotated −15 degrees and `(180,690)` rotated +12 degrees.

Add one ground shadow ellipse, 300 × 26 px, centered at `(600,925)`, Ink Black at 12% opacity.

The feeling is concentrated, capable work: Pip is actively entering and checking results while the desk, keyboard, status lights, and stacked papers connect the mascot to building and grading.

## 7. SVG BUILD NOTES

- Use `viewBox="0 0 1200 1200"` for every pose. Export each pose with a transparent background.
- Use flat vector illustration only: solid fills, clean geometric shapes, no gradients, no textures, no photorealism, no drop shadows, and no blur filters.
- One soft ground shadow ellipse is allowed per pose. Use Ink Black `#171A1A` at 12% opacity; do not use any other shadow.
- Use 14 px Ink Black strokes for every exterior outline, with `stroke-linejoin="round"` and `stroke-linecap="round"`. Use 5 px Ink Black rules for newspaper print and internal keyboard divisions. Use 8 px outlines only for small loose paper lines and the stacked desk newspapers where a 14 px outline would obscure the object.
- The only visible artwork text is the newspaper headline `DAILY // CIRCUIT`, the terminal string `> GRADE: PASS`, and the terminal string `> BUILD: LIVE`. The headline uses `DejaVu Sans Condensed, Arial Narrow, sans-serif`, weight 700, size 30 px, fill Ink Black. The two terminal strings use `DejaVu Sans Mono, Courier New, monospace`, weight 700, size 18 px, fill Terminal Green.
- Do not add a logo, wordmark, slogan, readable newspaper copy, labels, serial numbers, extra interface text, or decorative letters.
- The head casing, face screen, cap, antenna, newspaper torso, headline, paper fold, palette, and neutral proportions must be identical in all three poses. Only arm placement, hand placement, props, face expression, and listed background marks change.
- Layer order for each pose: background marks; ground shadow; rear limbs; torso and newspaper fold; front props; head and screen; cap and antenna; face pixels; hands; foreground desk or trophy overlaps; final small accents.
- The character must read clearly at 64 px through three recognition elements: the tilted black newsboy cap with green antenna bead, the black CRT screen with bright green pixel face, and the cream folded newspaper torso with its dark headline bar and gold lower-right seal.
- Preserve at least 60 px of transparent breathing room around the widest artwork in every pose. Ensure the trophy in Champion remains inside the canvas with its topmost outline no higher than y=165, and ensure all confetti remains inside x=130–1070 and y=150–950.

## 2. Brim fix


- Brim: flattened capsule-like path, 170 px wide × 40 px tall, centered at **(445, 300)** before rotation.
- Rotation: **−10° around (600, 300)**.
- Pre-rotation bounds: **x=360..530, y=280..320**.
- The right end overlaps the crown’s lower edge; the rotated left end projects clearly beyond the head casing, reaching approximately **x=363**.
- Crown shape and position, red stripe, and gold button are unchanged.

## CORRECTED SECTION 5 — CHAMPION

- Trophy size: **150 px wide × 160 px tall**.
- Trophy outer bounds: **x=625..775, y=165..325**.
- Trophy cup and rim: **x=625..775, y=165..280**.
- Trophy stem: **x=688..712, y=280..303**.
- Trophy base: **x=660..740, y=303..325**.
- Left raised arm terminates at hand center **(660, 318)**.
- Left hand bounds: **x=644..676, y=300..336**, gripping the trophy’s left base corner.
- Right raised arm terminates at hand center **(740, 318)**.
- Right hand bounds: **x=724..756, y=300..336**, gripping the trophy’s right base corner.
- Head casing, cap, torso, legs, feet, head tilt **+3°**, expanded smile, confetti, and sparkles are unchanged.

## CORRECTED SECTION 6 — AT WORK

- Monitor casing: **x=500..700, y=610..760**.
- Monitor screen: **x=520..680, y=630..720**.
- Screen text `> GRADE: PASS`: baseline **y=662**.
- Screen text `> BUILD: LIVE`: baseline **y=692**.
- The monitor’s top edge is now below the full `DAILY // CIRCUIT` headline, whose baseline remains **y=596**.
- Keyboard, desk, stacked newspapers, loose paper, background marks, head tilt **−2°**, focused expression, arms, desk front, legs, and feet are unchanged.

## 3. Corrected sections 5 (Champion) and 6 (At Work)


- Canvas: 1200×1200; character centerline x=600.
- Head casing: rounded rect x=420, y=280, w=360, h=270, r=55; rotated +3° around (600,420).
- Face screen: rounded rect x=448, y=325, w=304, h=184, r=24.
- Face eyes: 24×24 squares at (505,370) and (671,370).
- Expanded Champion smile blocks, each 18×18: (526,426), (544,444), (562,462), (580,462), (598,462), (616,444), (634,426), additional blocks at (544,462) and (652,444).
- Status pixels: 12×12 squares at (478,344) and (710,344).
- Cap crown dome: bbox x=405, y=216, w=390, h=112; rotated −10° around (600,300).
- Cap red stripe: follows the cap crown, rotated −10° around (600,300).
- Cap gold button: 22×22 centered approximately at (600,238).
- Antenna stem: x=594, y=228, w=12, h=52.
- Antenna tip: circle diameter 22 centered at (610,212).
- Cap brim: capsule w=170, h=40 centered at (445,300) before rotation; unrotated bounds x=360..530, y=280..320; rotated −10° around (600,300).
- Trophy overall bounds: x=505, y=180, w=190, h=160; centered at x=600; foreground layer in front of the head.
- Trophy rim: rounded rect x=529, y=190, w=142, h=24, r=12.
- Trophy cup: trapezoid with top edge (535,205)–(665,205) and bottom edge (556,290)–(644,290).
- Trophy left handle: curved handle from (535,214) through (505,214), (505,270), and (556,270).
- Trophy right handle: curved handle from (665,214) through (695,214), (695,270), and (644,270).
- Trophy stem: rounded rect x=588, y=289, w=24, h=38, r=8.
- Trophy base: rounded rect x=546, y=318, w=108, h=24, r=10.
- Left upper-arm centerline: (432,590) to (500,470).
- Left forearm centerline: (500,470) to (551,330).
- Right upper-arm centerline: (768,590) to (700,470).
- Right forearm centerline: (700,470) to (649,330).
- Left hand: standard cream mitten rect x=532, y=300, w=38, h=44; overlaps the trophy base left corner region x=546..570, y=318..342 by 24 px horizontally and 22 px vertically.
- Right hand: standard cream mitten rect x=630, y=300, w=38, h=44; overlaps the trophy base right corner region x=630..654, y=318..342 by 24 px horizontally and 22 px vertically.
- Arms and hands are mirrored about x=600.
- The trophy antenna tip and cap button are hidden behind the foreground trophy. The cap wings, face, and newspaper torso remain visible.
- Torso: rounded rect x=435, y=548, w=330, h=232, r=22.
- Headline: “DAILY // CIRCUIT”, 30 px, centered at x=600, baseline y=596; glyph bounds approximately y=574..596.
- Legs: centerlines x=535 and x=665, extending from y=775 to y=880.
- Left foot: bbox x=492, y=872, w=82, h=38.
- Right foot: bbox x=626, y=872, w=82, h=38.
- Ground shadow: Ink Black ellipse at center (600,925), 12% opacity.
- Exterior outlines: 14 px Ink Black; print rules: 5 px; small loose papers: 8 px.
- Confetti pieces: eight pieces at [(330,250),(390,170),(810,170),(870,250),(340,430),(860,430),(400,520),(800,520)], each 12×28, rotated respectively 18°, −12°, 12°, −18°, −20°, 20°, 14°, −14°.
- Sparkles: four four-point sparkles centered at (320,330), (880,330), (350,560), and (850,560), with outer bounds 28×28.

Verification: The left and right hands are symmetric about x=600 and visibly grip the trophy base corners. The left hand rect x=532..570, y=300..344 and right hand rect x=630..668, y=300..344 do not overlap either eye square x=505..529 and x=671..695, y=370..394, or any smile block within x=526..670, y=426..480. The trophy remains exactly x=505..695, y=180..340 and is centered at x=600. The head tilt is +3° around (600,420), the expanded Champion smile is retained, and all eight confetti pieces and four sparkles are present.

## CORRECTED SECTION 6 — AT WORK

- Canvas: 1200×1200; character centerline x=600.
- Head casing: rounded rect x=420, y=280, w=360, h=270, r=55; rotated −2° around (600,420).
- Face screen: rounded rect x=448, y=325, w=304, h=184, r=24.
- Focused eyes: 24×24 squares at (505,378) and (671,378).
- Focused five-block smile: 18×18 blocks at (544,444), (562,462), (580,462), (598,462), and (616,444).
- Status pixels: 12×12 squares at (478,344) and (710,344).
- Cap crown dome: bbox x=405, y=216, w=390, h=112; rotated −10° around (600,300).
- Cap red stripe: follows the cap crown, rotated −10° around (600,300).
- Cap gold button: 22×22 centered approximately at (600,238).
- Antenna stem: x=594, y=228, w=12, h=52.
- Antenna tip: circle diameter 22 centered at (610,212).
- Cap brim: capsule w=170, h=40 centered at (445,300) before rotation; unrotated bounds x=360..530, y=280..320; rotated −10° around (600,300).
- Torso: rounded rect x=435, y=548, w=330, h=232, r=22.
- Headline: “DAILY // CIRCUIT”, 30 px, centered at x=600, baseline y=596; glyph bounds approximately y=574..596.
- Monitor casing: rounded rect x=450, y=610, w=300, h=170, r=18.
- Monitor top clearance: casing top y=610 minus headline glyph bottom y≈596 gives 14 px clearance.
- Monitor screen: rounded rect x=468, y=628, w=264, h=112, r=12; fully inside the casing with 18 px left and right margins, 18 px top margin, and 40 px bottom margin.
- Monitor string 1: “> GRADE: PASS”, DejaVu Sans Mono bold, 18 px, Terminal Green; x=490, baseline y=665. Estimated width 140 px, ending at x≈630; screen inner right edge x=720.
- Monitor string 2: “> BUILD: LIVE”, DejaVu Sans Mono bold, 18 px, Terminal Green; x=490, baseline y=697. Estimated width 140 px, ending at x≈630; screen inner right edge x=720.
- Monitor status square 1: Terminal Green 8×8 square at (700,646).
- Monitor status square 2: Terminal Green 8×8 square at (700,670).
- Monitor status square 3: Terminal Green 8×8 square at (700,694).
- Keyboard: rounded rect x=500, y=764, w=200, h=30, r=8; key field x=512, y=770, w=176, h=18; it sits below the screen bottom y=740 and covers no screen text.
- Desk top: rounded rect x=405, y=790, w=390, h=24, r=8.
- Desk front: rect x=420, y=814, w=360, h=42; it overlays the legs from y=814 to y=856 and hides their lower halves while leaving the feet visible below.
- Legs: centerlines x=535 and x=665, extending from y=775 to y=880.
- Left foot: bbox x=492, y=872, w=82, h=38.
- Right foot: bbox x=626, y=872, w=82, h=38.
- Stacked newspapers: three rectangles at (820,760,150,18), (812,778,158,18), and (824,796,146,18), each with 5 px print rules.
- Loose paper: polygon with corners (910,700), (1010,708), (998,770), and (900,762), with an 8 px outline.
- Background marks: horizontal marks from (250,690) to (330,690), (870,690) to (950,690), (270,720) to (350,720), and (850,720) to (930,720); each 5 px Ink Black print rule.
- Left arm centerline: (432,590) to (470,690) to (500,750).
- Right arm centerline: (768,590) to (730,690) to (700,750).
- Left hand: standard cream mitten rect x=482, y=732, w=38, h=44.
- Right hand: standard cream mitten rect x=680, y=732, w=38, h=44.
- Ground shadow: Ink Black ellipse at center (600,925), 12% opacity.
- Exterior outlines: 14 px Ink Black; print rules: 5 px; small loose paper: 8 px.

Verification: The headline glyphs end at approximately y=596, and the monitor casing begins at y=610, giving 14 px of clearance; the headline is fully visible. Both monitor strings fit inside the screen: each is approximately 140 px wide, starts at x=490, ends near x=630, and remains inside the screen inner right edge x=720. All three 8×8 status squares at x=700, y=646, 670, and 694 remain inside the screen rect x=468..732, y=628..740. The keyboard begins at y=764, below the screen bottom y=740, and covers no screen text. The desk front hides the lower halves of the legs, while both feet remain visible below the desk.
