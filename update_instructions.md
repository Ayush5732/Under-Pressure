# Update instructions

## User's instruction

“when only 1 reply is availabe dont give choices in the game, prefill the text bar, abd only option left should be send, also the chats are loading and the player has to scroll to look at the texts make sure to add a typing option for each text that appears from the game once 1 block lands the player will read it , and he can see typing for next text to land, so he knows more info is comming instead of dumping all texts instantly.”

## Required behavior

- When exactly one authored reply is available, prefill the composer with it. Show Send rather than a one-item choice menu. Do not automatically send the player's reply.
- When several replies are available, show the supported conversational options; remove already-used replies within that discussion.
- Show a character-specific typing indicator before each incoming game message.
- Deliver messages separately, with reading time between blocks. Keep the typing indicator visible while a further message is pending.
- Keep the latest arriving message visible while the player is following the conversation. If the player scrolls up to read older messages, preserve that position and show a new-message indicator instead of forcing them down.
- Do not dump a whole scene into the chat at once. Do not require filler acknowledgements to advance an incoming sequence.

## Script review format

- Continue one selected story path through its ending.
- At genuine choice points, list all authored replies and bold the reply used on the selected path.
- When there is only one reply, show it directly as Alex's text, annotated as prefilled if needed; do not create a choice list.
- Include the manager's selected intervention. Respect actual budget locks and explain any departure from the first-option route.

## Agreed metric approach

Player-tendency evidence is distinct from story consequences. Track patterns across replies (budget awareness, detail, people development, independence, approval seeking, risk awareness and delivery focus), without declaring a personality from a single choice. Count each reply once and consider later follow-through.

## Timeline and Pulse

User instruction: “as the chat progresses the pulse needs to uodate timeline as well add realistic day additions, when something goes wrong add a scene to work weekends and the response of the tem changes based on the user behaviour, if the user is strict he will be met with retaliation/uncooperation if the user chooses good mentor path he it will be easier.”

- Pulse must update alongside story progress with the current project day/date, week within the sixteen-week schedule, upcoming milestones, elapsed time and remaining time to the agreed deadline.
- Advance time according to the work performed, not the number of chat messages. A conversation can happen on the same day; workshops, audits, implementation, retesting and training require believable elapsed days.
- Show date separators in chats when days change. Keep chat dates, Pulse dates and milestone dates consistent across private and group threads.
- Record delays, rework and recovery work on the Pulse timeline, including why a milestone moved. Keep the original deadline visible unless an extension is explicitly accepted.

## Weekend recovery scenes and team behavior

- When a setback creates schedule pressure that requires weekend work, add an authored conversation about the weekend recovery plan. Establish the concrete problem, work needed, affected people and expected time; weekend work should not appear after every minor issue automatically.
- Give the player conversational responses about how to request and organize the work. The team's reaction must depend on earlier behavior as well as the current request.
- A strict, punitive or dismissive player should meet pushback, retaliation or noncooperation consistent with each character: refusal of extra work, guarded replies, reduced discretionary effort, or unwillingness to volunteer and escalate uncertainty.
- A player who has followed a good mentoring path should find cooperation easier: team members are more willing to discuss availability, volunteer bounded help, share problems and propose a recovery plan.
- Preserve character-specific reactions. Maya, Jordan, Sam and warehouse coworkers should not all deliver the same response to the same leadership history.
- Good mentoring does not create unlimited capacity or remove personal commitments and fatigue. It improves trust and willingness to cooperate; weekend work still needs a feasible plan.
- Earlier support and follow-through must matter, rather than allowing one friendly sentence to erase a pattern of harsh treatment.
- Reflect the agreed weekend work, delays, workload and resulting readiness in Pulse. Do not count extra hours as verified completion automatically.

These are requested design changes; recording them here does not mean they have been implemented in the game yet.

## Daniel explains interventions

- Every manager intervention must be communicated to Alex by Daniel in an authored message, with a concrete, scenario-specific reason. Explain what changed, why, who made the decision, what is confirmed and what Alex can still challenge or negotiate.
- Do not present an intervention only as a finance notice, staffing notice or unexplained change in metrics. Daniel must address its impact and take part in the resulting conversation.
- Keep the human manager's private intervention selection hidden. Daniel's explanation is the in-world explanation, not a disclosure of the player or control that triggered it.

## Conditional negotiation bonus and intervention reversal

- Include one narrowly gated scenario where Alex can negotiate the intervention with Daniel. A successful negotiation may reverse the intervention; it must not be available on every route or guaranteed by a single polite reply.
- Establish a credible reason the decision can be reconsidered, the evidence needed, the decision-maker's authority, and the terms of reversal. Preserve already incurred consequences; reversing a decision does not undo elapsed time or completed work.
- For example, a budget-cut route could allow Daniel to seek restoration of authorization when Alex has built a credible delivery record, established why the cut makes agreed obligations unviable, and proposes a supported trade-off. This is a candidate design scenario, not an implemented or finalized trigger.
- Reflect any approved reversal and its conditions in the conversation, budget, milestone record and Pulse timeline.

## Bonus gates use the whole conversation history

- All bonus scenes require very specific authored combinations of choices. Evaluate earlier conversational replies as well as major story commitments: questions asked, wording chosen, private discussions, group replies, relevant casual exchanges and follow-through can supply evidence.
- Separate choices that directly change the story from wording that reveals player tendencies. Both contribute to bonus eligibility, but personality evidence alone does not automatically change project metrics.
- Evaluate combinations and order where meaningful: an evidence-seeking question, a respectful challenge, a realistic proposal and subsequent follow-through can together unlock a scene. No single generic keyword, repeated question or isolated flattering line should unlock it.
- Track each accepted authored reply once, with its scene, thread, context and evidence tags. Repetition cannot farm bonus eligibility.
- Define each bonus gate explicitly in code using recorded choices and project conditions. Do not use live LLM interpretation in the demo.
- All relevant authored chats can contribute; there must be no blanket restriction to major decision points. The free-text human-manager thread requires a separate explicit design if its content is to be assessed; do not silently add LLM analysis or keyword scoring there.
- Bonus eligibility should remain hidden from the player. The resulting conversation must feel earned by the relationship and evidence accumulated, rather than announcing a secret combination.

## Visible reply effects and mentor-only leadership assessment

- Before Alex sends any supported question or reply, show its exact current effect on the three visible metrics: client happiness, manager trust and board approval. Show explicit unchanged values where relevant. Calculate effects from current context, not generic labels that may be inaccurate on a different route.
- A single reply can affect multiple visible metrics. Explain the immediate effect briefly without revealing future outcomes or secret bonus gates. Pulse updates when the reply is accepted; later consequences are recorded separately rather than implied to occur immediately.
- Maintain additional internal leadership measures, visible only to the live mentor. These assess management behavior, accumulated tendencies and follow-through across the conversation.
- The live mentor must not disclose hidden metric names, numerical scores or bonus requirements to Alex. The mentor can discuss observed behavior and give practical advice without revealing the assessment mechanism.
- Keep hidden assessments out of the protagonist's API payload, UI, ordinary exports and feedback export. Any mentor assessment export must be a separate role-restricted feature, if later requested.

## Delivery success and management quality are separate outcomes

- Balanced or satisfactory visible metrics should support a successfully implemented project when the actual scope, evidence, acceptance and funding requirements are met. Do not declare implementation complete solely because three scores are high.
- A delivered project can still expose poor management: for example, concealment of uncertainty, unreasonable pressure, dependence on others, weak development of staff, or loss of team trust. Report delivery outcome and leadership assessment separately.
- A fall in client happiness must not automatically terminate every route. In specifically authored circumstances, strong manager trust, board approval and credible delivery evidence can sustain the project despite client dissatisfaction.
- Replace a universal client-happiness cutoff with explicit, scenario-dependent rules where warranted. Leadership backing, accepted trade-offs and a feasible plan must explain why a dissatisfied client's project can continue; high unrelated scores cannot erase missing scope, funding or unsafe release conditions.

## Manager priorities and realistic trade-offs

- The manager's current priority must shape which trade-offs and recovery plans are acceptable: cost/retention, schedule, usable delivery/quality, or team sustainability and development, as authored for that scenario.
- Daniel must communicate the priority in-world, including why it matters and any non-negotiable constraints. Do not make the player's outcome depend on an unexplained hidden priority.
- The live mentor's assessment can examine whether Alex understood the priority, challenged unrealistic demands constructively, and chose a feasible plan. A priority is not permission to ignore safety, agreed obligations or authorization.
- Different priority settings can produce different stakeholder reactions and acceptable endings for the same broad plan. Define these differences through explicit rules and conversations, not an arbitrary weighted total.
- Build the game as a management-learning simulation: decisions about people, evidence, capacity, money and commitments must interact. No single stakeholder score, personality tendency or universally correct reply should determine whether Alex is a good manager.
- Final reviews should cite specific observed choices and consequences. Private leadership judgments remain with the live mentor; player-facing lessons can emerge through conversations about the actual behavior and outcomes.

## Reconciliation with earlier metric instructions

The user now explicitly wants visible effects known before each reply. This supersedes any earlier assumption that all metric effects should remain hidden. Story-changing replies can retain conversational wording without decision labels, while their visible metric effects are shown accurately. Internal leadership evidence and bonus gates remain hidden from Alex. These requirements are design instructions, not a claim of implementation in the existing game.

## Revised project economics

- Base project scope/budget is $300,000 instead of $3,000,000. Divide all pre-existing monetary values by ten consistently: compensation packages, baseline commitments, audits, testing, training, recovery packages, budget cuts, retention targets and other expenses.
- Examples: Maya costs $60,000; Jordan costs $30,000; baseline commitments are $180,000; the former $200,000 board retention target becomes $20,000.
- The board separately controls a NEW $200,000 emergency reserve. This new reserve is not an old amount to scale again, and is not automatically part of Alex's spending authorization.
- Specific circumstances and recorded player choices can unlock a request for emergency funding. The amount requested, the board's decision and its conditions must be explicit; accessing the reserve need not mean drawing all $200,000.
- A justified request backed by consistently sound management can be approved without reducing board approval. Requests arising from avoidable mistakes or poor management reduce board approval according to context and severity.
- Evaluate the recorded decisions, evidence and circumstances rather than assuming any request for help is bad management. Daniel must explain the board's reasoning and approved authorization.
- Update all budget displays and dialogue consistently when implemented. Keep base-budget retention separate from any unspent emergency reserve so the reserve cannot falsely count as money Alex saved.

## Outcome distribution and two exceptional routes

User instruction: “keep only two threads of the story ... not needing additional funds and saving more than what the board wanted ... those need to be perfect where all the requirements are also met and the manager decisions are also good ... failure path don't have to be very common ... each path should lead to a learning ... or telling the player what he did ... doesn't have to be Learning.”

- Author exactly TWO exceptional story routes that meet every agreed requirement, need no additional/emergency funding, and retain more than the board's target from the base project budget. These are favorable-project-condition endings, not proof of consistently good management.
- Make these routes uncommon and dependent on bounded scope, a cooperative client, compatible mentor interventions and a feasible delivery plan. Assess management quality separately; savings alone must not imply good leadership.
- Define these as two canonical qualifying story routes, not two literal transcripts: harmless wording variations need not create additional exceptional routes unless they materially alter the required conditions. The exact qualifying combinations remain to be authored and reviewed.
- Most routes should allow credible completion or recovery with differentiated trade-offs, including conditional emergency funding, rather than funneling the player into failure after ordinary imperfect decisions.
- Outright project failure should be uncommon. It should follow consequential accumulated decisions or an unresolved critical constraint, with a clear explanation of what happened.
- Every completed route must reflect the player's actual choices and their consequences. Some endings can teach an explicit lesson; others can simply describe what Alex accomplished, sacrificed, handled well or handled poorly. Do not force a moral or corrective lecture onto every ending.
- Preserve the separation between project completion and management quality: successful delivery can involve damaged relationships, weak leadership, extra funding or reduced board approval; strong leadership can coexist with difficult compromises.
- Exceptional endings should feel earned. Ordinary successful endings should remain meaningful rather than being portrayed as failures merely because they required justified assistance.

These additions revise the design specification. The two exceptional routes, their gates and the rebalanced outcome distribution have not yet been implemented or validated.

## Exceptional high-cost, high-trust ending

- Add ONE narrowly gated exceptional ending in which Alex requests additional funding, exhausts the full approved emergency reserve, meets all agreed requirements and still retains strong management and board trust and earns a substantial bonus. The user permits one or at most two such endings; begin with one.
- This is a distinct exceptional ending from the two favorable-condition, no-additional-funding savings routes. Exceptional management must not be synonymous with spending the least.
- The client requirements and intervening conditions must credibly justify the cost. High spending caused by avoidable waste, poor planning, concealment or irresponsible promises cannot qualify.
- Require specific combinations of sound player decisions, conversational evidence, early escalation, honest reporting, responsible team management, approved funding requests and delivered acceptance evidence.
- Selected live-mentor interventions must affect eligibility. Define the relevant difficult circumstances and supportive or priority-setting mentor choices explicitly, rather than allowing all mentor settings to lead to this ending.
- The exhaustion of funds must be explained in the budget and timeline. Spend only within approved authorization, and distinguish approved unavoidable work from discretionary spending.
- Daniel and the board must explain why they still trust Alex: the requirements were difficult, the costs were justified and authorized, and Alex managed the constraints well and delivered the promised outcome.
- Award a strong bonus as recognition of management quality and delivery under difficult conditions, even though savings targets were not met. The bonus source must be separately authorized or outside the exhausted project allocation; do not silently overspend the project budget to pay it.
- The ending must explicitly show requirements completed and accepted. Exhausting funds and retaining trust alone is not proof of successful delivery.
- This should remain a rare earned ending, not a universal reward for requesting or spending the reserve. Its precise gates and bonus amount remain to be authored and reviewed.

## Clarification: favorable conditions versus exceptional management

- The two exceptional savings endings occur because the scope stays manageable and the client is cooperative. They demonstrate successful, economical delivery under favorable conditions; they do NOT automatically mean Alex is a good manager.
- Remove any earlier requirement or implication that these savings endings inherently certify good leadership. A separate mentor-only assessment may identify good or poor management on either route, based on actual behavior.
- The rare high-cost perfect ending is the difficult-client route: demanding requirements and difficult conditions consume the authorized funding, yet Alex satisfies the client, the board and management through strong judgment, justified spending, responsible leadership and accepted delivery.
- Evaluate outcomes against the conditions and choices that produced them. Do not rank players by raw savings or penalize justified high costs when scope and client behavior differ.
- In final conversations, acknowledge the favorable conditions on savings routes and the challenges successfully managed on the high-cost route, without making either a universal statement about personality.

## PlannedV1.1 playtest feedback — 12 October 2026

- Clearly indicate when Alex needs to move between a direct message and the group chat. Use an in-world notification that identifies the destination chat.
- When a character sends a DM, show a WhatsApp-style popup and a bright green badge with the number of unread messages. Clear that chat's unread count when the player opens that chat screen. Apply equally clear navigation cues when the next discussion belongs in the group chat.
- Reveal conversational choices progressively. Do not expose every question and commitment together at the start of a scenario.
- Do not reveal candidate-selection questions, options or candidate details before dialogue establishes that Alex needs to choose a candidate. Availability must follow what Alex has learned in the displayed conversation, including paced message delivery.
- Reframe the script more tightly: establish the situation and its purpose, then unlock relevant questions and decisions as the conversation reaches them. Keep optional information branches available when introduced, without revealing later story content prematurely.
- Collect further feedback while the user plays. These notes are queued for the next revision; recording them does not change the delivered game or the user's local installation.


## Cross-chat story and information routing — 12 October 2026

- Whenever story messages arrive in another chat, show a popup identifying and linking to that DM or group chat. Repeat this for every cross-chat story progression. Use green unread counts, cleared when the destination chat opens.
- Only show questions and replies belonging to the current conversation in its choice list. Questions addressed to another character must appear inside that character's chat, not in the chat the player is currently using.
- Use a distinct bright yellow or orange popup or chat indicator for an optional information branch available in another conversation. Selecting it opens that chat and reveals its relevant questions. Distinguish optional information from green notifications for actual new messages.
- Before showing an optional information cue, the current conversation must naturally identify who has the relevant information. Write this in the specific conversation's context, rather than repeating a generic instruction such as 'this information is with Daniel'. Reveal the cue only after that explanatory message is displayed.
- Make alternate paths discoverable while allowing the player to decide whether to consult the other character. Do not imply that every optional discussion is mandatory.
- These are queued playtest instructions; recording them does not change the delivered game.

## Information-gated replies and delayed consequences — 12 October 2026

- Limit available replies according to the specific information Alex has gathered and actually read in the conversation. A reply that relies on a fact must remain hidden until that prerequisite fact is known; do not reveal the missing information through the reply wording.
- Visiting a chat alone does not count as learning every fact in it. Unlock fact-dependent replies only after the relevant information has been delivered to the player.
- Preserve feasible replies for a player who decides with limited information, such as making an assumption, requesting clarification, or choosing an available plan. Do not force all optional information branches before every decision.
- Include conversational choices that initially sound ordinary or unobjectionable but create believable delayed consequences. Connect those consequences to the actual commitment or assumption, with subtle contextual clues rather than obvious 'bad choice' labels or arbitrary surprises.
- Keep immediate visible metric previews accurate, as already required. They do not expose the full later consequences or private assessments.
- Differentiate an uninformed assumption from a wrong interpretation of information the player did gather. Fact availability and the chosen reply must be recorded for later branch behavior and contextual review.
- This addition is queued for the next revision while the user continues playtesting.


## Evolving project brief, open questions and practical trade-offs — 12 October 2026

- Provide a Project scope/brief panel alongside candidate information. Begin with only the initial brief. Add confirmed requirements, constraints, responsibilities, dates, costs and agreements as Alex learns them on the chosen conversation path. Do not reveal facts from unvisited branches.
- Keep gathered information accessible in one place to support decisions. Identify its source and distinguish confirmed facts, assumptions, proposals and accepted changes; scope must not silently expand because a request was mentioned.
- Include a structured, visible but understated 'Open questions' or 'To confirm' section. Track gaps raised by the actual conversation, update them as choices introduce uncertainty, and resolve them when relevant information is gathered. Do not reveal every hidden story fact or future risk as an upfront checklist. A detail-oriented player can use this record to connect the broader project picture.
- Replace manager-trust and board-approval numbers on reply choices with grounded previews of practical effects, such as cost, schedule, workload, rework exposure or verification coverage. These previews must use known information and distinguish estimates from guaranteed changes. This supersedes the earlier instruction requiring exact manager/board metric deltas beside every choice. The user has not requested removal of those metrics from every other screen or specified removal of client happiness; do not assume that broader change.
- Harsh or rude choices may offer plausible short-term operational gains: faster immediate output, lower immediate spending, or less discussion overhead. Their later effects can include poorer quality, mistakes, guarded communication, fatigue, rework and reduced discretionary cooperation. Such gains are context-dependent, not guaranteed rewards for shouting.
- Separate delivery consequences from people-skill evidence. A short-term speed or cost gain does not automatically increase leadership or people-skill scores, and a supportive choice can incur real time or expense. Evaluate follow-through and circumstances rather than making every polite reply universally best.
- Preserve uncertainty where needed: do not disclose exact future consequences through a preview that Alex could not know. Give believable contextual hints and record actual effects when they occur.

## Assessment limits and clarification — 12 October 2026

- A fixed-information game cannot reliably infer whether a player deliberately misrepresented a fact, misunderstood it, or needed an explanation unavailable in the authored questions. Do not infer intent merely from exposure to a message.
- Record information shown, clarification requested, chosen commitments and observed consequences. Treat explanations of player reasoning as uncertain unless supported by an explicit authored response or live mentor discussion.
- Add context-specific clarification options, including alternate explanations and confirmation of an interpretation, before consequential decisions where warranted. If available clarification is insufficient, acknowledge that assessment limitation in the review rather than confidently labeling the player a poor decision-maker.
- These are queued playtest requirements; the delivered game has not yet been changed.


## Character-owned, decision-bound information opportunities — 12 October 2026

- Information questions belong to the person who can answer them, in that person's chat. For example, a question about how Elena plans to use a demonstration appears only inside Elena's conversation; it must not be offered as a general player-level action in the group chat or current unrelated DM.
- The current conversation provides a natural contextual hint and an optional yellow/orange cue. Alex must recognize the relevance, navigate to the appropriate chat and send the question to obtain the detail. Merely showing a cue or visiting the destination must not fill the project brief automatically.
- Add the answer to the project brief only as it is actually delivered/read. Keep information already gathered available after the decision.
- Bind each optional information opportunity to its unresolved decision. When Alex commits to that decision, immediately remove its optional popup/indicator and all now-expired questions or reply options associated with gathering information for that decision, even if Alex never visited the other chat.
- Do not allow post-decision backfilling of the recorded knowledge state. Future authored discussions may revisit a topic only as a new follow-up or recovery opportunity, with its own context and consequences.
- Expire optional-information notifications separately from real unread-message counts; do not erase genuine messages already sent just because a decision was made. Remove the obsolete optional route, not the conversation history.
- Record whether the opportunity was offered, consulted or expired, and what was known at commitment. Missing one optional discussion alone does not prove a personality trait; use accumulated observations and retain the fixed-dialogue assessment limitations.
- These requirements remain queued for the next revision during playtesting.


## Conflicting readiness claims, conditional feedback scene and deadline clock — 12 October 2026

- At selected decisions, the intern says their work is ready. Other relevant people can disagree if Alex actively consults them before committing. Give each person a credible basis: failed tests, incomplete acceptance criteria, unverified data, or user-readiness gaps. Their disagreement is not automatically known to Alex.
- Make the intern's claim plausible: the assigned implementation may be complete while broader acceptance remains incomplete. Avoid treating every incorrect readiness claim as dishonesty or incompetence.
- Where Alex gathers the relevant evidence and makes the appropriate readiness decision, unlock a specific bonus conversation with the intern. The opportunity depends on that decision's evidence and choice, not simply visiting every chat.
- In that bonus conversation offer authored encouragement/coaching and confrontation/shouting responses. Encouragement produces no immediate speed, cost or efficiency gain in this scene; it is the sound people-management response, with later trust, disclosure or cooperation effects grounded in follow-through.
- The shouting response produces a bounded short-term speed and throughput/efficiency gain in this authored situation. Keep speed distinct from quality-adjusted efficiency: later guarded communication, rushed mistakes, fatigue or rework can offset the gain. Do not imply shouting always improves performance in real life.
- Show believable operational trade-offs without exposing future secret consequences or making the supportive option instantly superior on every visible measure. Record actual effects in the timeline, project evidence and later character reactions.
- Add a literal visual clock/deadline indicator with green, yellow and red states based on schedule slack and delivery risk. Include text labels and time remaining so the meaning does not depend on color alone. It represents the simulated project timeline, not a forced real-time countdown.
- Keep the clock consistent with Pulse, elapsed project days, outstanding work and the currently accepted deadline. An extension updates the accepted deadline while preserving the original deadline record. Green means feasible slack, yellow means at-risk margin, and red means overdue or insufficient time for the current plan; precise thresholds must be tied to the schedule model.
- These are queued playtest additions, not changes already made to the delivered build.





