# [Game Title] — QA Test Plan & Bug Report Suite

**Target Build Version**: v0.1.0-alpha  
**QA Lead**: QA & Playtesting Engineer  
**Sign-off**: Producer, Lead Programmer  

---

## 1. Test Suite Matrix

### 1.1 Core Mechanics & Physics Verification
| Test ID | Area | Scenario | Expected Outcome | Pass/Fail | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-001** | Movement | Normal walk & sprint across flat terrain | Velocity transitions smoothly, no jerky frames | Pass | Tuned at 8.0 m/s |
| **TC-002** | Movement | Jump off ledge within 80ms coyote window | Jump registers successfully while airborne | Pass | Coyote time verified |
| **TC-003** | Movement | Input jump 100ms before landing | Player jumps immediately upon touching ground | Pass | Jump buffer verified |
| **TC-004** | Collision | High speed dash into 45-degree angled wall | Character slides along plane without penetrating | Pending | Stress test needed |
| **TC-005** | State | Pause game during mid-air attack animation | Physics freeze; resume continues without state corruption | Pending | Edge case test |

---

## 2. Bug Report Defect Template

```markdown
### [BUG-001] [Category] Brief Description of Issue

- **Severity**: [P0 - Blocker | P1 - Critical | P2 - Major | P3 - Minor / Polish]
- **Discipline**: [Code | Art | Design | Audio | Level | UI]
- **Repro Rate**: [e.g. 5/5 (100%), 3/5, Intermittent]
- **Build / Commit**: [git commit hash or build version]

#### Steps to Reproduce:
1. Launch game from main menu and start Level 1.
2. Navigate player to the edge of the collapsing bridge (coordinates: X: 124.5, Y: 12.0).
3. Execute a double jump while simultaneously pressing the Pause key.
4. Unpause the game and observe player physics state.

#### Expected Result:
The player should resume falling and trigger the water hazard respawn volume.

#### Actual Result:
The player remains suspended mid-air in the falling pose indefinitely; inputs become unresponsive (Softlock).

#### Attachments / Logs:
- `logs/crash_20261001.log`
- `media/screenshots/bug_001_softlock.png`
```

---

## 3. Playtesting & Balance Questionnaire

1. **Player Agency & Responsiveness**: Did the controls feel direct and snappy, or sluggish?
2. **Pacing & Tension**: Were there long stretches of boredom or frustrating difficulty spikes?
3. **Clarity & Affordance**: Was it immediately obvious where to go and what objects could be interacted with?
4. **Delight Moments**: Which mechanic or visual moment felt most rewarding?
