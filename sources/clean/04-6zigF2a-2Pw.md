# CMU AI Agents 2026: 4. Memory and Skills for Agents

- Видео: https://www.youtube.com/watch?v=6zigF2a-2Pw
- Длительность: 1:15:22
- Дата публикации: 20260908

## Расшифровка

[00:05] Okay, welcome back everyone.
[00:08] >> So, um the first assignment is out and
[00:10] uh as Graham said, we we have credits
[00:12] available for you to to work on it for
[00:14] those of you who are enrolled in the
[00:16] class. Do you folks have any logistic
[00:21] questions? Cool. Okay. So we talked in
[00:24] the last lecture about how agents can uh
[00:26] choose what to retain within their
[00:28] context window as a way of you know
[00:31] storing information within a task and
[00:34] using that to um to determine what's
[00:36] important to do better within the task.
[00:39] So a big part of today is going to be
[00:41] about how can agents go beyond the
[00:43] context window and store information
[00:48] across tasks in external stores um that
[00:50] will be useful for them to improve
[00:53] performance on tasks in the future. And
[00:56] this is going to be skill induction. Um,
[00:58] and uh, we'll build on some some work
[01:01] that was done in the past on memory
[01:04] systems for agents. Um, and show how to
[01:06] apply those to to agents. But there's
[01:09] also another view on skills. And skills
[01:11] are a way for people to write
[01:13] instructions for an agent that can
[01:15] encode kind of like best practices or
[01:18] the knowledge that you have about how a
[01:20] task should be done. And these are
[01:22] actually going to be complimentary to
[01:25] each other. Um so we'll cover it just a
[01:27] small amount in this lecture but um you
[01:30] can imagine a system that um is sort of
[01:32] having a human in the loop um that's
[01:36] relying on the agent to uh propose some
[01:38] potential best practices from the
[01:40] experiences that it has a person edit
[01:42] those and goes back and forth or vice
[01:45] versa like you know having a skill and
[01:46] instruction that's written by a person
[01:49] be refined by the agent based on
[01:51] experience. So yeah, it's a lot of
[01:53] different viewpoints, but hopefully by
[01:54] the end of the lecture, you'll see how
[02:01] So let's just start off with some
[02:04] motivation about why you might want to
[02:06] remember things from one task to
[02:09] another. So say that we have an agent
[02:12] that's carrying out tasks in a website
[02:14] like a shopping site and you might give
[02:16] it a task like add Sony headphones to my
[02:20] wish list. So when we cover guey agents,
[02:22] you'll we'll get into the details of,
[02:25] you know, the representation space, the
[02:27] action space for how a system like this
[02:29] works. But at a high level, it's going
[02:33] to be producing actions like um uh
[02:36] navigating to the store website, finding
[02:38] the search box for it, typing some text
[02:40] in that search box, and then clicking
[02:42] search. And that's going to be the part
[02:43] that like searches for the headphones,
[02:45] right? And then we'll do something with
[02:48] them. We'll find the ones that match the
[02:49] request the user had and put them into
[02:51] our wish list.
[02:53] We might have another task that we carry
[02:55] out in the future like find the wireless
[02:57] keyboard price range. And if we're doing
[02:59] that on the same site, a lot of the
[03:02] actions are going to be reused, right?
[03:03] We'll go to the store, we'll find the
[03:05] search box, we'll search for the
[03:07] different product but in a similar way
[03:09] and then we'll do something different
[03:11] with it like you know getting the prices
[03:13] and reporting those back to the user.
[03:16] But if it's difficult for the agent to
[03:18] figure out how to do this search, once
[03:20] it knows how to do it, it should be able
[03:23] to reuse that knowledge in the future to
[03:27] be more effective on future tasks.
[03:31] So a lot of structure recurs and today
[03:32] is going to be about how can we
[03:35] represent this shared structure. So for
[03:38] example, is it best to just uh keep kind
[03:41] of the raw actions that the agent
[03:43] produced when it was carrying out this
[03:46] shared subtask or is it better to try to
[03:48] abstract it into for example a code
[03:51] function which could be run as a
[03:54] blackbox or maybe tested or even like
[03:57] hierarchically call other functions.
[03:59] We'll also be interested in how can the
[04:01] agent like determine which parts of a
[04:05] task should be reused in the future.
[04:10] And um as we're you know any time we
[04:12] have a memory that we're building up
[04:14] from experience, there's questions about
[04:18] um how do we grow that memory? Do we are
[04:20] we always adding to it? What happens if
[04:22] we get some conflicting information or
[04:25] we find a better way to do something? We
[04:26] might want to make edits to it. we might
[04:28] want to delete things if they no longer
[04:30] seem to apply. So, how can we um kind of
[04:34] manage the life cycle of these skills um
[04:36] and these subtask representations that
[04:39] are learned?
[04:40] [snorts]
[04:42] So, I'd say there's three general ways
[04:45] that we can get agents to update. So,
[04:47] the first one we covered in the last
[04:50] lecture. It's um just what you maintain
[04:53] in the context window of the model. So
[04:55] this is um you know in the standard
[04:58] React style way. It's the history of the
[05:00] past observations and actions that
[05:02] you've taken, messages you've gotten
[05:03] from the user, feedback from the
[05:05] environment, and you need to you need to
[05:08] choose like what to retain given kind of
[05:10] the limitations of the context window
[05:15] and the model's ability to use that. So
[05:17] uh we talked a lot about like compaction
[05:19] and methods for managing what's in that
[05:21] context window. Today we're going to be
[05:24] focusing on storing things outside of
[05:26] the context window. So even with like
[05:28] really long context windows that we have
[05:32] now of like a million tokens uh for um
[05:34] multiple for like carrying out multiple
[05:36] tasks with an agent um you're going to
[05:39] exceed that context window and you want
[05:41] to remember things from past tasks to
[05:44] help you on future ones. So if we are
[05:47] storing things outside of the window, um
[05:49] that's going to look something like a
[05:51] database um that needs to be managed um
[05:55] in some some way or um like a file
[05:58] system that the agent can access. And uh
[05:59] this lecture is going to be about
[06:02] methods for um putting things into those
[06:05] types of storage and um using them and
[06:08] updating them. And then the final way is
[06:10] going to be like actually making uh
[06:12] updates to the weights of the model.
[06:15] Right? So this looks more like standard
[06:16] supervised fine-tuning or reinforcement
[06:18] learning. We'll cover that in a few
[06:21] lectures later on. But each of these has
[06:25] like pros and cons. So um I think like a
[06:28] main pro of using external artifacts is
[06:31] that they're like they can be ported
[06:34] across models, right? So if you um have
[06:38] a description of the way to search for a
[06:40] product um that could be used by any one
[06:43] of a number of different models um
[06:45] within an agent framework. Whereas if
[06:47] you're actually making updates to the
[06:49] weights of the model that's just an
[06:51] update for that specific model and it
[06:54] doesn't transfer to others. So external
[06:57] artifacts are also more inspectable by
[07:00] people. Um, so you could write down best
[07:02] practices or how to search on a site.
[07:04] The agent can use that. The agent could
[07:06] also propose, you know, kind of text for
[07:08] that and you could look at it and make
[07:11] changes to it. So there's it's easier to
[07:13] kind of like have an interface between
[07:16] the person and the system if your um
[07:18] method of updating, if your method of
[07:21] remembering is interpretable.
[07:25] Any questions about this?
[07:27] How many folks have uh have used skills
[07:29] in their interactions with the coding
[07:31] agent? Like how many of you Okay, so
[07:33] most folks have. How many of you are are
[07:36] writing the skill yourself?
[07:38] Okay, so maybe about half the folks who
[07:40] are using skills. How many of you have
[07:42] uh gotten an agent to write a skill for
[07:45] you? Okay, so a lot of folks actually
[07:47] have. Yeah. What are some things that
[07:49] what how what's your experience been for
[07:51] the agent writing the skills? How often
[07:53] have you been able to use it just right
[07:55] out of the box? The thing that the agent
[08:01] anyone have any spectacular failure
[08:05] cases or spectacular successes? So just
[08:07] repeating that for the recording like
[08:09] sometimes the models will write too much
[08:11] in the skill like they'll kind of
[08:15] overinfer the what should be done and
[08:16] then when that's handed off to another
[08:18] model it will kind of follow it to the
[08:20] letter and do a lot more than you
[08:22] actually wanted it to.
[08:31] >> Cool. Oh yeah, go ahead. I mean in cases
[08:33] when you're like trying to like a
[08:34] production issue for like a particular
[08:37] system if you give it like three or four
[08:39] support
[08:41] and you tell it that look at how people
[08:43] have this issue in the past create a
[08:46] skill for yourself
[08:48] other agents could use to it in the same
[08:49] way
[08:50] >> and that's
[08:51] very
[08:52] >> oh nice
[08:55] >> okay cool yeah so instructing it to like
[08:57] get write the instructions for another
[08:58] agent it's good enough it's sort of like
[09:00] simulating what the agent would do.
[09:02] Yeah, that's interesting. I've sometimes
[09:04] found that the models are like pretty
[09:06] bad at kind of like simulating the
[09:08] theory of mind that you know another
[09:10] person or an agent would have when they
[09:11] like look at instructions, but they get
[09:13] a lot better when you prompt them to do
[09:16] that. Cool.
[09:19] Okay.
[09:21] Yeah. So, a few different like types of
[09:24] experience that we might want to retain
[09:27] for agents. So the first is like the
[09:29] episode and this is you know just the
[09:31] sequence of observations that you get
[09:33] from the environment from the user and
[09:36] the actions that are taken and this is
[09:38] sort of like the maximum fidelity right
[09:40] you're just you're retaining everything
[09:42] you have all the specifics of that
[09:44] particular environment and the
[09:46] particular instructions that the user
[09:49] gave also going to be like the most
[09:51] costly right it'll need the most tokens
[09:54] to represent and you probably don't need
[09:56] all of that right? Like uh just like
[09:58] when we're doing you know supervised
[09:59] learning we don't want to retain every
[10:02] detail we want to abstract to the things
[10:04] that matter to generalize um in the
[10:06] future.
[10:10] So we could also retain some facts like
[10:13] um some knowledge about the environment
[10:16] um or about the user and in the early
[10:19] work on memory systems uh a lot of it
[10:21] was focused on retaining facts. So like
[10:24] a user is interacting with an assistant
[10:26] and maybe gives some personal
[10:28] information like how old they are or
[10:31] where they live. The system can retain
[10:33] that in its memory and then use that
[10:36] fact to improve future interactions. If
[10:39] you've um used uh like Anthropic or
[10:42] Chatbt's uh memory systems, uh they're
[10:44] doing this basically, right? Like you
[10:46] can go into the settings, you can view
[10:48] the memory that they have about you and
[10:50] there's, you know, a text representation
[10:53] there from a model that's produced those
[10:55] facts um from your past interactions.
[10:57] Looks a little bit like compaction in
[10:59] some way. It's generated by an LLM. It
[11:02] gets stored in this external thing.
[11:04] And then the final one is more specific
[11:07] to agents. So it's about like how do you
[11:11] do part of a task um in a way that's
[11:13] abstracted from the details of the task.
[11:15] So like in the example we looked at
[11:17] before, how do you search for products
[11:20] on a particular website without maybe
[11:22] retaining the details of searching, you
[11:24] know, the particular product that you
[11:26] searched for? And so there's a lot of
[11:28] choices about how you would represent a
[11:30] skill. Is it just text? Is it kind of
[11:32] the actual actions that you took? Um or
[11:35] could it even be code?
[11:37] And of course, skills are only going to
[11:39] be useful if you're going to be doing
[11:47] So we could think about like um memory
[11:49] and skills and the intersection between
[11:52] them. So memory is just something that
[11:53] we're saving from the agents
[11:55] interaction. So for example, what's a
[11:57] previous product that you purchased on a
[12:00] site? A skill would be reusable
[12:02] knowledge about how to act in an
[12:04] environment. um which could be
[12:06] represented in one of a variety of ways.
[12:08] Like it could be, you know, if you're
[12:12] releasing a um application um by pushing
[12:15] it to production, here's a checklist
[12:17] that you need to go through before you
[12:19] do that. So, a skill could be written by
[12:22] a person like in this example. But we
[12:24] could also have um a combination of
[12:27] memory and skills. So we could induce
[12:29] skills from the agents past experiences
[12:32] and store those um and then use those to
[12:34] hopefully do better in the future. So if
[12:35] the agent searched successfully for a
[12:39] product in the past um and uh yeah and
[12:41] if it was successful, if we think that
[12:43] it was successful, then we could pull
[12:45] out something that looks like a skill to
[12:47] guide the agent in the future. And we'll
[12:49] get a lot more concrete about what this
[12:50] looks like through the rest of the
[12:56] So we can think about skills as
[12:58] instructions where uh skills as
[13:00] instructions might be written by a
[13:02] person um for encoding their own you
[13:05] know preferences or might be
[13:07] organization policies like this is the
[13:10] way that we write and test code in this
[13:14] particular company. Um and human
[13:16] authored skills um we know where they
[13:18] came from. we have more maybe control
[13:21] over the quality but it takes you know a
[13:22] lot of time to write them and to
[13:25] maintain them. If we're learning skills
[13:28] then the agent is producing them. Um and
[13:30] this is helpful because we can do this
[13:32] in an automated way. Maybe we can have
[13:34] like a loop where we induce the skill.
[13:36] We try to use the skill to redo the same
[13:38] tasks. We see if things get better on a
[13:41] metric. Um, but it can be, you know,
[13:42] potentially noisy too and have, you
[13:44] know, especially if you're using the
[13:46] skills for some other agent like we
[13:48] talked about in those examples everybody
[13:50] gave, um, it could maybe have unintended
[13:57] Okay, so let's talk first about uh,
[13:59] humanridden skills and um, the standards
[14:02] for these and the ways that they're used
[14:05] in incurrent agents. So probably a lot
[14:07] of it sounds like a lot of you have
[14:11] experience with this already. Uh so
[14:13] maybe you've been using these in the
[14:15] context of an example kind of like this.
[14:18] Uh there's this nice blog post from open
[14:20] hands that has guidance on using skills.
[14:23] Um for those of you who um who haven't
[14:25] used skills yet or if you you know like
[14:28] some suggestions on how to uh how to
[14:30] have best practices for creating and
[14:33] using skills. But they have this
[14:35] motivating motivating example of say
[14:37] that you find yourself like always
[14:39] giving similar instructions to a coding
[14:44] agent. Um so you um want the you want to
[14:46] check the code that has been written
[14:47] using one of a couple different
[14:49] llinters. You want to give type hints.
[14:51] You want to use a particular type of
[14:53] dock strings. And you want to apply
[14:56] piest to all the functions. So if you're
[14:58] always doing this, you could always type
[15:01] this guidance into the system. Um, but
[15:04] you know, a kind of natural and faster
[15:07] way to do this would be to just have the
[15:10] like store the guidance as a text file
[15:12] and then have the agent use that
[15:16] guidance um as an instruction. So you
[15:17] should reach for a skill when you want
[15:19] to do something repeatedly following
[15:21] kind of like a fixed specification. And
[15:23] the agent's going to choose how to
[15:25] interpret this specification in context,
[15:28] but the um general instruction is the
[15:33] And the way that this is implemented in
[15:36] the current standard for skills um which
[15:39] is called agent skills is just as a
[15:41] collection of files which the agent is
[15:47] And here's an example of of that. So if
[15:50] we are constructing a skill for Python
[15:53] review um we'll have a folder which has
[15:56] a structure like this. So skills have
[15:58] this standard structure where they'll
[16:00] have a skill.md file and you have to
[16:04] have that. Skill.md um is a markdown
[16:06] file that starts with um some YAML
[16:09] metadata. So you need to have a name for
[16:11] the skill and you need to have a short
[16:14] description uh which is going to give
[16:16] guidance to the language model about
[16:18] when the skill should be applied. And
[16:20] we'll see in a slide or two about how
[16:22] the model gets access to this
[16:26] information in the YAML header. And then
[16:28] um after the header you'll have a much
[16:30] more detailed description of um how the
[16:32] skill should be applied which would for
[16:34] example you know list um here are all
[16:35] the llinters that you should apply
[16:37] here's how testing should be done and so
[16:41] on. So you have to have skill.mmd. You
[16:44] also have a few other um folders which
[16:46] are optional but can contain some extra
[16:49] resources for the agent to use as it
[16:51] carries out the skill. So there's
[16:54] scripts which has executable code. So
[16:57] for example, if you had like a Python
[16:58] script that would run a llinter, you
[17:00] could put it in there and then describe
[17:03] it in this skill.md file. There's also
[17:05] references, which would be sort of like
[17:07] supplementary documentation that maybe
[17:09] you don't you you don't need to use it
[17:12] every time you use the skill. Um, but
[17:15] you'll have maybe a reference to that
[17:16] documentation in the skill file. The
[17:18] agent could load it as needed from the
[17:21] references folder. And then assets
[17:22] basically just has like, you know,
[17:24] additional templates or resources like
[17:25] if you're, you know, doing something
[17:28] that involves like Ginga and you need
[17:32] the agent to load that conditionally.
[17:34] So this can be a lot of information,
[17:37] right? And we um don't want to fill up
[17:40] the context window of the model um with
[17:42] all of the possible skills that it could
[17:44] use. So there's a mechanism called
[17:46] progressive disclosure which is going to
[17:50] just show relevant parts of skills to
[17:52] the agent as they're needed. So the
[17:56] first level is um the metadata in this
[17:58] YAML file. Uh so the name and the
[18:01] description and that's always going to
[18:04] be um shown to the model in the system
[18:07] prompt if the skill is loaded if it's
[18:10] available to the model to use. So you
[18:13] need to be kind of concise in this uh
[18:15] description. Um so that if you have a
[18:16] lot of skills you don't fill things up
[18:19] too much.
[18:21] There's the second level which is the
[18:23] rest of the text in the markdown file
[18:26] and um that'll be loaded conditionally
[18:29] if the model decides that the skill is
[18:32] relevant um and uh decides to read the
[18:35] rest of the file via a tool call. We'll
[18:37] see an example of that in a minute. And
[18:38] then the next level is sort of like all
[18:41] the resources in here which will also be
[18:45] loaded um using tool calls. So you kind
[18:46] of need to have enough information in
[18:49] the skill.md file for the model to be
[18:51] aware that it should look into these
[18:54] additional folders to get more resources
[18:56] um when it's carrying out the skill. Any
[18:59] questions about this and you'll
[19:01] implement this in assignment one or
[19:03] maybe some of you are already starting
[19:05] on implementing that.
[19:20] like what if that takes too much of that
[19:21] effect performance?
[19:24] >> Yeah. So if you have a lot of skills
[19:27] even if the skill metadata is pretty
[19:28] short could it affect performance? Yeah,
[19:31] it definitely can. Um so you want to
[19:33] keep the number of skills somewhat small
[19:36] and maybe just load them conditionally.
[19:39] um in one of the state-of-the-art
[19:41] agents, Hermes agent, I think the I'm
[19:43] not sure the number of skills, but like
[19:44] the total length of the skill
[19:46] descriptions in the system prompt is
[19:49] like 3,000 tokens. Um there's some
[19:50] papers that we'll see in a little bit
[19:52] that show that if you have too many
[19:54] skills, um it can make performance
[19:56] worse. Like adding in irrelevant skills
[19:58] can drop performance um because, you
[20:00] know, the context gets longer. The model
[20:02] might be distracted by things that are
[20:04] actually irrelevant. So yeah, you
[20:06] definitely need to be careful about the
[20:08] number of skills, but um I think it
[20:10] would be pretty rare to have like 10,000
[20:12] or a thousand skills. Generally, it's,
[20:14] you know, smaller and you would maybe
[20:16] load skills as needed for like the
[20:19] software tasks that you're carrying out.
[20:20] >> Yeah.
[20:23] >> How sensitive are those triggers?
[20:26] >> Yeah, that's a great question. How
[20:28] sensitive are the triggers? So the the
[20:31] triggers will be tool calls that will be
[20:34] generated by the model. And so whether
[20:37] they get called or not is a function is
[20:39] totally dependent on the model. Um and
[20:43] you know the model's ability to predict
[20:44] that it should be triggered based on the
[20:48] past context and what it knows about the
[20:50] skill. So that you know depends on the
[20:51] model depends on the description you
[20:53] write and um that's why we need
[20:56] evaluations for this. Um and one of the
[20:57] papers that we'll look at takes a step
[20:59] in that direction.
[21:02] >> Yeah.
[21:11] >> Yeah. Uh skill.md is a standardized
[21:13] name. So the the standard is called the
[21:16] um I think the agent skills standard and
[21:19] um you like models agents are trained to
[21:21] to use that agent frameworks are trained
[21:25] to load that. Um so yeah you um if you
[21:27] want to use an alternate format well
[21:29] first put it you know as close to this
[21:31] as you can but you could do you know if
[21:34] you have particular if you have
[21:36] particular um things that you want like
[21:38] in the references folder you could
[21:41] describe them in skill.md and like all
[21:42] this is just going to be instructions to
[21:44] the language model so it could be robust
[21:47] to other configurations also especially
[21:50] if you describe them.
[22:02] >> Yeah, why markdown? It it is a balance
[22:04] of machine and human readability, I
[22:12] >> Yeah, that's a great question. Could
[22:14] there be better formats than than
[22:16] skill.md?
[22:19] Yeah. Do you have things in mind?
[22:24] I think like um so uh I mean it's just
[22:26] like linear right um it's you can have
[22:28] hyperlinks which is good you can embed
[22:32] images too um
[22:36] >> yeah um but uh like it's difficult to
[22:38] you know represent things that are
[22:40] dynamic so like maybe you want to
[22:42] illustrate to the model like um
[22:43] different ways the data could be
[22:46] visualized um you know maybe that would
[22:47] be better with like a JavaScript
[22:49] interactive JavaScript application or
[22:52] something like that. Um, yeah, you
[22:53] could, you know, have that be sort of
[22:55] like a code file here that gets
[22:58] executed. Um, but and maybe like
[23:00] referenced in the markdown. Um, so I
[23:02] think like markdown is sort of the best
[23:04] attempt at having something that's
[23:06] general and like readable, but then you
[23:08] would rely on the language model to
[23:10] interpret other formats.
[23:12] >> I think in the scientific literature
[23:14] that uh Daniel's going to talk about,
[23:16] there's basically two ways. There's
[23:18] textual skills and programmatic skills
[23:20] and the textual skills appear in the
[23:22] markdown and the programmatic skills
[23:24] appear in the script. So it kind of it's
[23:27] pretty broad if you consider those.
[23:30] >> Yeah. Cool.
[23:30] >> Yeah.
[23:32] >> Does anyone do
[23:35] to not have to put it all in context?
[23:36] For example, if you're making an agent
[23:39] that modifies cloud infrastructure, you
[23:41] work at some big bank and have a billion
[23:45] things in AWS and it would be nice to be
[23:47] able to just ask the model to modify
[23:48] something, but then because it's a
[23:50] billion things, you can just have a
[23:52] billion tools for every small component
[23:54] available. Yes.
[23:56] >> So looks like something
[23:59] would
[24:01] do. Yeah, definitely in some of the
[24:03] research papers that so the question was
[24:05] like do people retrieve from large
[24:08] collections of skills. Um and yeah
[24:09] definitely in some of the research
[24:11] papers that we'll look at um they do
[24:13] that um either using you know just like
[24:17] a text embedding based retrieval or
[24:18] doing something that's more kind of like
[24:20] domain conditional like we know these
[24:23] skills apply to this site so when we're
[24:25] interacting with that site we'll load
[24:27] those skills. Yeah, I imagine production
[24:30] systems do this too, but um yeah, I
[24:32] don't have any references off the top of
[24:36] my head for that. Cool. Okay, so we'll
[24:38] uh just uh kind of quickly to show you
[24:41] how progressive disclosure works. Um we
[24:44] first need to give the model access to
[24:46] this level one, right? Let it know what
[24:49] skills are available. And you'll have a
[24:51] system prompt that looks something like
[24:53] this. This is just taken from Hermes
[24:55] agent which is sort of like a standard
[24:58] open- source um agent that is able to
[25:02] use and induce skills and you'll um kind
[25:04] of describe what skills are. Uh you'll
[25:06] tell the model about this skill view
[25:09] tool which it could use to read the rest
[25:12] of the markdown file and then you'll
[25:14] list out all the skills that you have.
[25:16] So there's just two skills here. Um,
[25:18] there's a code quality skill and a
[25:20] workflow skill. And that's just the YAML
[25:28] So, um, the model is able to use tool
[25:30] calls to, you know, expand the rest of
[25:32] the skill. And here's what that might
[25:35] look like. So, it always has the index
[25:38] of skills in the system prompt, but it
[25:41] could choose to make a tool call to open
[25:43] the Python review skill. um if that
[25:45] seems relevant to you know the user
[25:48] asked for a review of some Python code
[25:51] and then it's going to like um you know
[25:55] get that markdown file insert it as a
[25:57] message to the system as an observation
[26:01] the result of that skill view tool. Um
[26:02] the system might choose to run something
[26:05] from the scripts directory um and then
[26:06] it'll get the result of running that
[26:08] script as an observation put it in the
[26:11] window um and might choose to you know
[26:13] like view additional files within that
[26:21] Okay. So yeah, we these questions that
[26:23] we had about like you know could
[26:25] additional skills hurt um are skills
[26:28] being triggered in the right place. Uh
[26:30] we answer questions like this by
[26:33] building evaluations and um the the work
[26:35] on this is a little bit um new. It's
[26:38] sort of ongoing but um a really great
[26:40] first effort in the space is called
[26:43] skills bench and what they do is they um
[26:46] collect a bunch of skills uh from uh
[26:47] various sources online. they actually
[26:51] get like 2 million skills. Um, and
[26:53] they'll also have people write tasks
[26:56] which seem like they could benefit from
[26:59] skills. Uh, and so they'll like get 400
[27:02] tasks and um those are going to be
[27:04] written independently from the skills,
[27:06] but they'll have the task annotators
[27:08] choose from this pool of skills ones
[27:11] that seem like they could apply to the
[27:13] tasks. And so you'll have kind of like a
[27:16] small set of curated skills. um and
[27:19] you'll supply those skills to an agent
[27:21] as it's trying to solve the task and
[27:23] they'll evaluate this on like um you
[27:26] know four different agent frameworks uh
[27:28] with I think like 18 models something
[27:31] like that and they'll just see like does
[27:34] having the skills um improve performance
[27:36] over not having the skills across all
[27:39] the tasks for a given agent framework
[27:42] and model combination right so this will
[27:44] evaluate you know it'll implicitly
[27:47] evaluate the skill quality but will be
[27:50] designed to evaluate is a model and
[27:52] framework able to you know use the
[27:54] skills appropriately and they're trying
[27:56] to choose the skills. So they have like
[27:59] a filter um which checks to see that for
[28:01] a small subset of models the performance
[28:05] on the tasks does improve when you give
[28:07] models access to the skills and then
[28:08] you're seeing if that's also true for
[28:11] kind of a wider set of frameworks and
[28:16] Yeah.
[28:21] Does the general setup make sense? Cool.
[28:24] So on average, you know, with this cur
[28:27] curated set of um skills, uh the average
[28:29] pass rates on these tasks using like
[28:31] humanridden verification criteria does
[28:33] increase. And so you can see like the
[28:37] solid bars to the shaded bars across a
[28:39] bunch of different models um and
[28:44] frameworks. Um but actually uh ski like
[28:48] tasks that require fewer skills to solve
[28:50] benefit more from having the skills
[28:53] available than ones that require more
[28:56] skills. Um and so this is partly a
[28:57] difficulty thing but also partly that
[28:59] the models might be getting distracted
[29:02] by having more skills available. And you
[29:03] could imagine that it's getting much
[29:06] worse with like a much larger number of
[29:08] skills. Um we'll see some more evidence
[29:12] for that later on in the lecture.
[29:15] And actually skills still hurt on a
[29:17] number of the tasks for particular model
[29:20] types. Um so the model might be using
[29:22] the skill inappropriately which could
[29:24] actually make it do the task in a way
[29:25] different than what the person
[29:27] specified. So this kind of motivates the
[29:29] importance of like checking to see if
[29:31] the skills that you wrote are actually
[29:38] So skills can come from, you know, a
[29:40] bunch of different sources. They could
[29:42] be bundled with the harness. Um, they
[29:45] could be written by a person. Um, and a
[29:46] lot of you have done this, it sounds
[29:48] like, and you then, you know, kind of
[29:50] install it in a in a way that's
[29:52] specified by the framework that you're
[29:55] using, but they can also be created by
[29:58] the agent. And, um, Hermes has a skill
[30:00] manage tool. um open hands as a skill
[30:03] creator uh command that help work you
[30:06] through the process of creating a skill.
[30:08] And when you're creating a skill, I
[30:09] think it's really important to base that
[30:13] skill on some prior interactions that
[30:15] you've had rather than trying to just do
[30:19] it sort of a priori. Um and actually
[30:21] there's some results in the skills bench
[30:23] paper that show that models when they're
[30:25] tasked to create a skill by themselves
[30:27] just based on a task description,
[30:29] they're really bad at it. and it
[30:31] actually makes performance worse. So, as
[30:32] a person, you're probably better because
[30:34] you kind of like know the way that you
[30:36] want it to be done, but it's generally
[30:38] best to base it on, you know, past
[30:40] things that you've done because when
[30:41] you're doing a task, it'll reveal some
[30:43] things about the way you want it to be
[30:47] done that you might not know in advance.
[30:49] So there's a nice case study of this um
[30:52] from the open hands blog post on how do
[30:54] you like so you have this code review
[30:56] skill that you've created. How do you
[30:58] check and see if it's working and then
[31:01] improve it if necessary.
[31:04] So this is focused on like reviewing
[31:07] poll requests and what what you could do
[31:09] is like um after the review is produced
[31:12] by the agent then a person is going to
[31:14] go through the poll request and look at
[31:16] each of those review comments and either
[31:19] address them or not. And you can apply a
[31:21] modelbased judge after that and count up
[31:24] how many of these were like actually
[31:26] used by the person which will give you a
[31:30] sense of how good the pull request was.
[31:33] And you can like um do this over a large
[31:35] number of pull requests that were
[31:37] created and then reviewed by the agent
[31:40] using this skill. And um if you do this
[31:43] over um you know like hundreds or
[31:46] thousands of examples, you'll get a lot
[31:47] of evidence about what's working and
[31:49] what's not, you can summarize all of
[31:52] that with a reasoning model um and use
[31:55] that to like for example identify that
[31:58] it's not helpful to um you know produce
[32:00] code that ignores the repo conventions.
[32:02] people did like incorporate those
[32:04] changes quite a bit. And then you could
[32:06] like have the model propose some updates
[32:11] to the skill file that will make the you
[32:14] know reviews produced by the system more
[32:26] Okay.
[32:28] So next we'll talk about how do we get
[32:31] models to automatically remember things
[32:32] from their past experience and then
[32:35] we'll use that to like build on um to
[32:37] talk about inducing skills from
[32:40] experience.
[32:43] So this is this is an old paper. This is
[32:46] from 2023 um but it was pretty
[32:50] influential. Um and it's uh it's one of
[32:53] the first papers it's called MEMGPT.
[32:56] It's one of the first papers to uh
[32:56] [snorts]
[32:59] introduce a way that you can manage
[33:01] memory outside of the context window of
[33:03] a language model. So this is like a
[33:05] really a systems inspired paper. I think
[33:07] we talked about a couple lectures ago
[33:08] about you know kind of having like
[33:10] memory hierarchies like you know
[33:13] something that is fast to access which
[33:15] for the language model is the context
[33:17] window and then something that's like
[33:20] larger but but slower and in this
[33:22] setting that would be like an external
[33:25] store of of facts and back when this
[33:27] paper was written uh a few years ago
[33:29] context windows were even shorter like
[33:33] you know 8,000 tokens um so this sort of
[33:35] approach was really well motivated even
[33:37] for just interacting with like an
[33:39] assistant system. Um nowadays you know
[33:41] our context windows are larger but what
[33:43] you want to store in them is also much
[33:45] larger. So this sort of approach is
[33:48] pretty well motivated for agents too.
[33:50] But the basic idea here is that you're
[33:54] going to have like a um you'll have you
[33:55] know the system instructions which don't
[33:58] get updated. you'll have a working
[34:02] context um which is going to uh pull
[34:05] things from an external memory um and
[34:07] also you'll be storing things to this
[34:10] external memory and those reads and
[34:12] writes are going to be controlled by
[34:15] tool calls from the model
[34:17] and um you'll also you know have like a
[34:20] separate storage for the actual messages
[34:22] that the system received um but that's
[34:23] going to be controlled in a pretty
[34:25] similar way to this uh this memory over
[34:26] fax
[34:28] So, what this actually looks like, sorry
[34:29] it's a little bit hard to read with the
[34:33] brightness in here, but like if you um
[34:35] you might uh have an interaction with
[34:37] the model where the user like mentions
[34:40] six flags and um the system could
[34:43] produce a tool call that searches within
[34:46] this storage for past mentions of six
[34:48] flags from its past interactions. It'll
[34:50] take those and it'll put them into this
[34:53] like working context. Um and then the
[34:55] model um this working context is stored
[34:57] within the context window of the
[34:58] language model. So the model will be
[35:01] able to use those as it outputs its
[35:09] But it's important to be able to do more
[35:11] than just like add to memory because for
[35:14] example like um maybe you're talking to
[35:17] the system about your job. you say I
[35:20] work at X, but then if you change jobs
[35:22] later on, you want the system to be able
[35:25] to like use the latest information.
[35:29] And um this paper called me zero uh
[35:32] introduces a way for memories to be
[35:35] updated as well. Um so the way that this
[35:37] works is you'll have like messages
[35:40] coming in and um each time you get a
[35:42] message, you'll apply a language model
[35:45] to extract some memories from it. um
[35:47] some like potential facts that you might
[35:49] want to store or update and you'll have
[35:54] an external uh database store um and
[35:56] you'll try to check and see do I have
[35:57] anything in that database store that's
[36:01] relevant to these um facts that I pulled
[36:03] out of these messages. So you'll
[36:06] retrieve the top K and to do this you'll
[36:07] use like an embedding based retriever
[36:09] model like you know the ones we talked
[36:11] about a little bit ago. um you'll pull
[36:15] out similar facts like um six flags for
[36:18] example or like um I work at X and
[36:21] you'll apply a language model to check
[36:23] for all of these extracted memories from
[36:28] these latest messages um do they um are
[36:29] they present in these similar retrieved
[36:33] memories? If they're not present then we
[36:36] should potentially add them in. um if
[36:39] they are an update to something that's
[36:42] there, we should replace what's stored
[36:44] for that with the new thing. If it
[36:46] negates something that's already there,
[36:48] like for example, you say, "I work at
[36:50] X," but then later on you say, "I got
[36:52] laid off," you might want to just delete
[36:54] that fact rather than um than updating
[36:58] it. Um or if it's not relevant at all,
[37:01] you would just ignore it.
[37:03] And um I'll refer you to details or for
[37:06] the paper for for details about this um
[37:07] because the details also change with
[37:10] with agentive systems but I think the
[37:13] idea that um it's useful to be able to
[37:15] like update knowledge as well if you
[37:17] have conflicts is potentially pretty
[37:18] useful.
[37:21] So, um, does anybody remember something
[37:24] from the lecture on context management
[37:27] that had a similar goal to this being
[37:31] able to update or delete memory?
[37:33] Yeah.
[37:36] Uh, hashing.
[37:38] >> Yeah. Yeah. Basically, does anybody
[37:45] Yeah. Yeah, it's hashing in the sense
[37:48] that there we had like key values and
[37:50] queries, right? Um and we were like
[37:52] storing values which were vectors. Um
[37:55] here we're storing like text um as
[38:00] Yeah.
[38:03] So the Delta paper actually did this,
[38:06] right? like um linear attention is only
[38:11] able to append um values to your um
[38:14] what's effectively your memory but Delta
[38:18] um uh like effectively retrieves um
[38:20] things that are stored for particular
[38:22] queries and then changes them changes
[38:24] the vectors that are stored for for them
[38:26] and that helps improve performance. So
[38:29] this is sort of like a textbased analog
[38:32] of that that has a similar goal.
[38:35] Yeah, you could also think about like um
[38:37] for the third type of learning for
[38:39] updating the weights of a model, it's
[38:41] potentially helpful there to be able to
[38:44] forget stuff also. Um especially if you
[38:45] have kind of like conflicting knowledge
[38:47] and and people are starting to develop
[38:49] some approaches for that like unlearning
[38:56] Okay, so those are some foundational
[38:59] papers about memory um that were
[39:01] developed for assistance
[39:05] for agents. Um feedback on trajectories
[39:09] can be really useful. So this paper
[39:11] called reflection was um a really
[39:15] impactful it's a really uh it's a really
[39:18] pretty simple but effective um the way
[39:20] to get agents to use feedback and
[39:22] potentially do better. So, it's
[39:24] definitely worth knowing about. It's a
[39:25] good thing to implement if you're
[39:27] working on a project that might want an
[39:29] agent to be able to benefit from its
[39:32] past experiences. Um, and the way it
[39:34] works is we're trying to improve the
[39:37] performance of an agent given multiple
[39:40] attempts on a particular task. So, say
[39:42] that you're asking the agent to like um,
[39:44] you know, search for a product on a
[39:47] website. It makes one attempt at it. um
[39:50] it says that it's finished and you're
[39:52] able to get some feedback about whether
[39:54] it was likely correct or not. So that
[39:56] could come from like a person looking at
[39:58] it. It could come from applying a model
[40:02] as a judge. Um but given that feedback,
[40:04] you'll want the model to try again and
[40:06] try to do better.
[40:09] And what this paper does is show that
[40:11] natural language feedback um on the
[40:14] attempt can be a really helpful thing
[40:16] for the model to condition on in its
[40:18] second attempt. So like if it's trying
[40:20] to answer this question about what was a
[40:22] particular series of battles, it might
[40:24] just mention one particular battle and
[40:27] then the feedback that's given um
[40:28] generated by a language model based on
[40:31] knowing this is incorrect and looking at
[40:34] the question and the answer might be um
[40:36] you gave just a single battle rather
[40:38] than a series. So as you can imagine
[40:40] this would be really helpful feedback
[40:42] for the model to condition on as it you
[40:44] know does another attempt at this task
[40:47] and it can get it correct. Um and the
[40:48] paper shows that you know conditioning
[40:50] on this natural language description of
[40:53] what went wrong can be really helpful.
[40:56] So we can generalize this also to um the
[40:59] agent improving as it does different
[41:00] tasks. Right? This is improving on the
[41:04] same task. But you could imagine um
[41:07] feedback might be generally helpful to
[41:09] improve performance on similar tasks as
[41:11] long as the feedback's like sufficiently
[41:17] And the final way that we can like um
[41:20] have agents uh improve or you know kind
[41:21] of the final foundational thing for
[41:25] helping agents improve um is remembering
[41:27] trajectories uh like entire
[41:29] trajectories, entire episodes that
[41:31] they've done in the past and using that
[41:34] to shape what they do on future tasks.
[41:35] There is a bunch of papers that have
[41:37] done this. We have some links to them at
[41:39] the bottom of this slide. Um, but the
[41:41] key thing in all of them is you'll have
[41:43] some collection of like training tasks
[41:45] and those tasks could be like a
[41:47] collection of demonstrations or they
[41:49] could be produced by the agent as it's
[41:52] carrying out tasks one at a time. Um,
[41:54] and you'll pull all of those tasks
[41:57] together. Maybe you'll additionally like
[42:00] um generate some text that describes uh
[42:01] feedback from them sort of like
[42:03] reflection did on the last slide. And
[42:06] you'll have that pool of experiences.
[42:09] And then when you get a new task um that
[42:12] comes in, you'll retrieve from this uh
[42:15] set of trajectories and um maybe
[42:17] generated text about them to find
[42:18] something that's relevant for the task
[42:20] that you're carrying out. You'll put it
[42:22] in the context window of your model and
[42:24] it'll generally help you to do better.
[42:26] Um so this is sort of like rag for
[42:29] agents, right? Um and uh it's pretty
[42:31] effective.
[42:38] Yeah.
[42:40] >> What do you mean by trajectory in this
[42:42] case is like sequence of calls.
[42:44] >> Yeah. Yeah. So a trajectory generally
[42:48] for an agent is the sequence of um like
[42:49] messages that it gets from the
[42:50] environment or the user. So the
[42:53] observations um the actions that it
[42:58] takes like the tool calls and um and uh
[42:59] potentially also you know the chains of
[43:01] thought that it produces. So one way to
[43:03] think about it is basically just like
[43:07] all the sequence of um of uh messages um
[43:10] in the context window of the model
[43:13] >> and you retrieve it by image
[43:14] differently. You can do this regular
[43:18] embedding retrieval or compare to
[43:20] process sequences and do some set
[43:22] comparison.
[43:24] >> Yeah. What are the different ways that
[43:26] you could do retrieval? So typically you
[43:28] want the model to you're giving the
[43:30] model the description of a new task that
[43:33] it should carry out. So you have just
[43:35] that text description and you'll embed
[43:38] that um with an embedding model and
[43:40] you'll retrieve um based on the
[43:43] descriptions of other tasks that each
[43:44] have like a trajectory associated with
[43:47] them and maybe you'll also constrain
[43:49] that to be like we'll just retrieve the
[43:51] tasks for this particular domain that
[43:54] we're working in. Um yeah, good
[43:57] question. Any other questions about this
[43:59] approach? Generally, this is sort of
[44:01] like a whole class of approaches. Um
[44:03] there's different ways to instantiate
[44:05] it. Um the details like how do you build
[44:07] up the experiences? How do you do the
[44:10] retrieval? Um but just want to kind of
[44:13] give you a sense that if we have past
[44:15] successful trajectories and we show
[44:17] those as examples to the agent, it can
[44:24] Okay. So with that we kind of have the
[44:26] foundation for talking about um actually
[44:30] inducing skills. Um so
[44:32] we can think about skills as being like
[44:36] parts of a task that are reusable across
[44:38] different tasks. So at the very
[44:40] beginning we talked about like searching
[44:44] for a product and that might look
[44:47] something like we tell the agent show me
[44:50] results for this particular query and
[44:52] the agent might produce a chain of
[44:54] thought like this and then it might
[44:57] produce these particular actions that
[44:59] actually interact with the web page like
[45:02] um uh clicking on this element
[45:04] identified by this particular ID which
[45:06] is the search box typing a query in
[45:08] there and and clicking on another
[45:11] element which is like the actual button
[45:13] to search.
[45:17] And this uh chunk of a task might be
[45:19] reused on future tasks. Like if I say
[45:22] what is the price range for um this
[45:25] particular item, it might need to do
[45:27] these same exact steps again as well as
[45:31] some additional ones afterwards.
[45:33] And so we can think of a skill as being
[45:36] um a specific like reused part of the
[45:38] task.
[45:44] Can anybody think of any issues with
[45:57] just
[46:02] that's right. Yeah. So, like if the
[46:04] element ids on the page change, the
[46:06] skill will break. And you know, there's
[46:07] a number of ways that that could happen.
[46:09] Like, you know, maybe the elements are
[46:11] maybe it's the same page, but things are
[46:13] just numbered differently. You can make
[46:14] some changes to the action space to deal
[46:16] with that. I think JY will talk about
[46:19] that in his lecture. But like if we go
[46:21] to a different website that has like a
[46:24] different search interface um it's going
[46:26] to break and we'll see some examples of
[46:33] Yeah. So we'll generally compare as
[46:35] Graham said text versus code as ways to
[46:37] represent skills.
[46:40] I want to briefly highlight some uh
[46:42] really cool papers um from the past that
[46:44] I think kind of like lay a foundation
[46:47] for skill induction um for learning
[46:49] skills from experience. Uh, one is
[46:53] called um Voyager and um they're
[46:55] controlling an agent in Minecraft. Um,
[46:58] and they're using uh code as a way to
[47:01] control the agent where the code
[47:04] functions um implement things like um
[47:07] crafting a particular item or combating
[47:10] a zombie. And representing these like
[47:13] subtasks as functions allows functions
[47:16] to call each other. So that as the agent
[47:18] like learns functions for simple things,
[47:21] it can then like compose them calling
[47:22] them in other functions and you can
[47:26] carry out increasingly complex tasks.
[47:28] There's also a line of work um from the
[47:31] program induction community um that that
[47:32] does this. I think a really nice
[47:35] representative of this is um uh work
[47:38] called dreamcoder and a few papers that
[47:41] built on it. And there you're um sort of
[47:43] uh you have basically like grammarss
[47:45] over things that you're constructing um
[47:50] like objects um and you uh like have uh
[47:53] some examples of complete objects which
[47:54] are constructed using like very
[47:56] low-level functions and you search for
[47:58] recurrent patterns in that you find
[48:00] patterns that can be abstracted into
[48:02] functions and you do that repeatedly and
[48:04] you're sort of like compressing the
[48:07] programs that construct these objects.
[48:09] And then there's also some follow-ups to
[48:11] this that uh integrate like large
[48:15] language models, Python code, and uh
[48:19] natural language descriptions too.
[48:22] And some of the same ideas in those
[48:24] papers are also useful for agents that
[48:27] are um using language models to interact
[48:30] with the world. A typical way that we'll
[48:33] evaluate systems for inducing and using
[48:35] skills is an online learning setting. So
[48:37] when you're interacting with um an
[48:40] agent, you are maybe having it carry out
[48:43] a bunch of tasks in succession and some
[48:44] of those tasks are going to be similar
[48:47] to each other. You want the system to be
[48:49] able to learn from your interactions
[48:51] with it and then be able to do better in
[48:54] the future, right? So um this is an
[48:56] online learning setting where we'll have
[48:58] tasks come in one at a time. So for
[49:00] example, like you might say, add a Sony
[49:03] Bluetooth headphone to my wish list. And
[49:05] we'll be building up a memory of skills
[49:08] um incrementally as we solve those
[49:11] tasks. So um there will be an induction
[49:13] step that we'll talk about in a slide or
[49:17] two. And that induction step will
[49:20] create a skill like search for a product
[49:22] and add a product to the wish list that
[49:24] are useful for solving this particular
[49:26] task.
[49:28] And um you know maybe we have another
[49:32] one like this task here and we can apply
[49:34] those skills on future tasks like this
[49:37] task might also involve searching for a
[49:39] product and hopefully we'll do better on
[49:43] that task given that we had this skill
[49:46] induced from the previous task
[49:49] and so on. So what we're interested in
[49:51] is if we can measure success on each of
[49:53] these tasks, is our success rate like
[49:55] getting better and better? Are we able
[49:58] to solve increasingly complex tasks um
[50:00] as we're learning from experience and
[50:03] building up um uh representations of the
[50:07] ways to do these simpler tasks? Any
[50:18] So the papers that we'll look at for the
[50:20] rest of the lecture look at sort of
[50:24] different parts of this space of um uh
[50:26] learning skills from experience having
[50:28] this library and ask questions about
[50:29] what should we do with the skills like
[50:33] after we've um induced them. So there's
[50:34] generally like a learning step where
[50:37] we'll have these uh tasks coming in.
[50:39] We'll try to get a skill out of them.
[50:41] will decide whether to store that skill
[50:43] um in the memory that we're building up
[50:47] over time. There's um the step of like
[50:50] actually using this memory of skills to
[50:52] potentially improve performance on the
[50:55] tasks that we're carrying out. And then
[50:57] finally, we might want to, you know, if
[50:59] we're getting too many skills, we might
[51:01] want to try to simplify those, like
[51:03] delete the ones that aren't being used,
[51:05] or if they're too specific, we might
[51:07] want to make them more general. um or
[51:09] like consolidate and merge multiple
[51:11] things together.
[51:16] We'll go a little bit deeper into one
[51:19] paper um that I think is pretty
[51:22] representative of ways for inducing
[51:24] skills. Uh it was also done here at CMU
[51:27] as work led by Zora Wong who will be
[51:29] giving a guest lecture on some other
[51:31] topics a little bit later on in the
[51:33] course. Um but this paper's called agent
[51:37] workflow memory and um the way it works
[51:40] is it we applied it to web tasks. Uh
[51:43] this is work with with Graham also um
[51:45] and me and uh we applied this to web
[51:50] tasks and you have a query like this and
[51:51] you know tell me the number of reviews
[51:54] that our store received so far and when
[51:55] the agent's carrying this out these are
[51:57] the actual tool calls that it'll
[51:59] produce.
[52:02] So we have this sequence of tool calls
[52:04] and we want to try to identify which
[52:06] parts of this might be potentially
[52:08] reusable in the future
[52:10] and you can probably guess how we do
[52:13] this. We ask a language model to take a
[52:15] look at the sequence of tool calls and
[52:17] identify ones that seem like they might
[52:24] And we'll have the model output what we
[52:26] call workflows um which are sort of like
[52:29] a textbased representation of skills
[52:31] text and actions. And a workflow will
[52:33] have like a description of the subtask
[52:37] like searching for a particular item.
[52:40] And then um it'll have the sequence of
[52:43] actions that you use to do that. And
[52:45] we're having the model make this a
[52:46] little bit more general so that it could
[52:49] apply to like searching for other terms.
[52:52] So we have it use like create a template
[52:56] that can abstract out some parts of the
[52:59] um initial action sequence. You might be
[53:00] thinking like this is starting to look
[53:03] like code, right? That's true. Um and a
[53:05] little bit later on we'll compare code
[53:08] to this also and show how that can be
[53:11] better in some ways but also uh make
[53:14] things a little bit more uh fragile.
[53:17] A pretty important part of this is we'll
[53:20] um apply a judge model to this
[53:23] trajectory to decide um have the judge
[53:25] predict whether the trajectory seem to
[53:28] be correct or not. And we'll use that to
[53:30] determine whether we should actually add
[53:32] the workflows that were induced to the
[53:34] memory. Um because we don't want to be
[53:36] um remembering things that were
[53:38] incorrect because those might steer the
[53:41] model wrong in the future.
[53:50] Okay. And
[53:51] so
[53:54] the way that we'll um give the model
[53:56] access to these uh collection of
[53:59] workflows um is just by sticking them in
[54:01] the context window of the model. So this
[54:03] looks a lot like you know this agent
[54:05] skill standard. Um you have choices
[54:07] about whether you show everything or
[54:09] whether you show just you know kind of
[54:12] the text description. um and what you do
[54:14] there could depend on how many skills
[54:16] you have and you know the context length
[54:21] So um for the sake of time I I'll skip
[54:24] over this induction prompt but we do
[54:27] find that um having this memory of like
[54:31] past uh subtasks um can help to improve
[54:33] the performance of the agent as it's
[54:36] learning online. So on the x-axis here
[54:39] we have like um different tasks in a
[54:41] fixed ordering from this benchmark
[54:43] involving interacting with like a map
[54:45] tool and the blue line here is the
[54:47] baseline agent that doesn't have a
[54:49] memory that sort of converges to around
[54:52] you know like 10% accuracy on these
[54:55] tasks and the labels here are the tasks
[54:57] that are being solved by the agent
[55:00] correctly. Um and then this black line
[55:03] which adds in this memory of um subtasks
[55:05] improves pretty substantially and it's
[55:07] able to um you know this gap emerges
[55:09] between the two but it's also able to
[55:10] carry out these like increasingly
[55:13] complex tasks eventually doing things
[55:14] like you know finding a hotel near this
[55:17] location showing me the walking path um
[55:19] that the baseline agent just isn't able
[55:28] So this is using, you know, sort of this
[55:31] mix of text and example actions to
[55:33] represent skills.
[55:36] But we could also consider using code,
[55:38] right? And both of these are
[55:41] implementations of a search product um
[55:44] function. And
[55:45] if we're using just this text and
[55:47] examples, this is going to be in the
[55:50] context window of the model. and then
[55:51] it's going to be needing to produce
[55:54] these tool calls um in a new context,
[55:56] right? As it tries to carry out the same
[55:59] subtask. So, it's flexible like the
[56:02] model could choose to insert a
[56:04] particular search term to search for a
[56:06] different product. If the website has
[56:09] changed and we no longer have like this
[56:12] particular um element for the search
[56:14] box, then the agent could choose to use
[56:18] the correct one instead. Um, but it also
[56:19] means that the agent needs to like
[56:21] actually produce all of those tool calls
[56:25] itself. If we're using code, the agent
[56:28] could actually just call this function
[56:30] as a tool, right? If it passes in the
[56:31] right arguments and if the functions
[56:32] correct, then it doesn't have to do
[56:34] anything. It doesn't have to produce all
[56:36] of those low-level actions itself. Um,
[56:38] the tool will just do that as it
[56:40] executes in the environment. Can anybody
[56:43] think of uh some pros and cons of using
[56:45] a function like this as a representation
[57:01] >> It's very rigid.
[57:04] >> Yeah, it is very rigid. So like um the
[57:07] model will need to the model calling
[57:09] this tool will do exactly these three
[57:11] steps and there's no room to to deviate
[57:14] from it. Um yes that's a main call
[57:17] that's a main like con to it but we also
[57:19] get a lot of the pros of using code
[57:22] right so like we can nest functions it
[57:24] can be hierarchical we can actually like
[57:27] generate test cases for that specific
[57:30] function too independent from the entire
[57:32] trajectory that it's executed in. And we
[57:34] can do things like you know refactoring
[57:37] also.
[57:41] So uh Zora has another paper um called
[57:43] inducing programmatic skills or agent
[57:46] skill induction which um which do this
[57:47] and it looks pretty similar to the
[57:49] approach we were using to induce these
[57:51] textual workflows. So you have a
[57:53] trajectory like this with these tool
[57:56] calls and we'll have the language model
[57:59] um we'll we'll just use the fact that
[58:01] language models are also good at
[58:04] generating code and we'll um prompt the
[58:07] model to generate functions which
[58:11] abstract a lot of the um uh behaviors in
[58:13] this trajectory and these are real
[58:15] examples. So the language model will
[58:18] write this search reviews function and
[58:20] um a doc string for it and then you know
[58:23] it has these low-level tool calls as um
[58:25] lines in the function. This other one
[58:27] for open marketing reviews but we'll
[58:29] also have it generate sort of a rewrite
[58:31] of this original trajectory that uses
[58:34] those tools. So a really nice thing
[58:37] about um code is that we can test it by
[58:39] executing it. So instead of applying the
[58:41] judge to the original trajectory like we
[58:43] did before, we can have the language
[58:45] model. Well, we can execute this
[58:47] generated abstracted code and then apply
[58:50] the judge to the end result that you get
[58:52] from that. And if that appears to be
[58:54] correct, that's sort of like a stronger
[58:57] indicator that the skills, these code
[58:59] skills that you induced are also
[59:00] correct.
[59:02] And if they are, then we put them in the
[59:05] memory and they become usable to the
[59:08] language model just as tools. So this is
[59:10] a way of like building up a tool library
[59:12] that the model's able to use on future
[59:15] examples and um we show that it also you
[59:26] Yeah. So a nice thing about um code
[59:28] skills is that they allow testing just
[59:31] of the skill by itself. Um there's this
[59:33] nice paper called skillw weaver which
[59:36] does this. Um, so this is sort of some
[59:40] pseudo code for the uh the loop that I
[59:42] just showed you where you have a task,
[59:45] you um propose some set of like code
[59:50] skills for it and then you'll try to use
[59:52] those skills to execute the task. You'll
[59:54] get an episode, you'll apply a reward
[59:58] model to it. Um, and if it succeeds,
[01:00:00] then you can put all those induced
[01:00:02] skills into your memory. But if not,
[01:00:04] then you could make some revisions to
[01:00:06] it. And there's a number of ways that
[01:00:10] skills might not succeed, right? So, um,
[01:00:12] one thing we could do is like apply a
[01:00:15] code llinter to an induced skill. So,
[01:00:17] here's a real example from the paper.
[01:00:19] There's this induced skill called
[01:00:21] identify pill. Um, you know, for like
[01:00:24] interacting with a drug website. And
[01:00:26] this uh function like takes a lot of
[01:00:29] arguments like you know the um the make
[01:00:31] of the pill the color but in the initial
[01:00:33] version of this skill that the agent
[01:00:35] wrote it actually didn't use all the
[01:00:36] parameters. So like it ignored this
[01:00:38] color parameter. So you could get
[01:00:41] feedback from a llinter on this skill
[01:00:43] and then sort of in the reflection type
[01:00:47] way um condition on that and then like
[01:00:50] you know uh create an updated version of
[01:00:53] the function and store that or like try
[01:00:55] executing that and store that. You could
[01:00:57] also use feedback from this reward model
[01:01:00] and condition on that when you're um
[01:01:02] making these revisions to the skill 2.
[01:01:04] So these are some nice benefits of code
[01:01:06] um that can be advantages even if you
[01:01:08] know the actual code function itself is
[01:01:14] Another nice benefit is that because
[01:01:17] these functions that are induced are now
[01:01:19] tool calls, it can really reduce the
[01:01:21] number of times that your agent needs to
[01:01:23] interact with the environment. So here's
[01:01:27] an example from um Zora's uh ASI paper.
[01:01:31] We have this uh task like uh updating a
[01:01:34] couple addresses on a page and for the
[01:01:37] base agent you have to you know like do
[01:01:39] all the very low-level actions of
[01:01:41] navigating through all these forms
[01:01:44] typing the particular um things from the
[01:01:47] address. But if we have this model that
[01:01:50] has induced these code skills, you can
[01:01:53] and this is a real example from uh from
[01:01:55] the work where we induce this navigate
[01:01:57] to address settings and update address
[01:02:00] details functions. We can actually solve
[01:02:03] this task in three steps where we um you
[01:02:05] know assuming that this is a good fit
[01:02:08] for the site. Um we can just call these
[01:02:12] two functions and um complete the task.
[01:02:14] Um, and the agent is actually much
[01:02:17] faster because it doesn't need to
[01:02:19] reobserve the website and then generate
[01:02:21] the tool call, then reobserve the new
[01:02:23] website, generate the new tool call. Um,
[01:02:26] as you'll probably see in the guey um,
[01:02:29] lecture that JY is giving, um, a really
[01:02:31] big bottleneck for these models is
[01:02:33] actually the number of times that they
[01:02:34] have to interact with the site because
[01:02:37] these images take up a lot of tokens and
[01:02:39] actually producing a chain of thought
[01:02:41] um, before each action takes up a lot of
[01:02:43] tokens too. All of those have to be
[01:02:45] generated. So efficiency is really
[01:02:48] important here.
[01:02:50] And um in this work we did find so we
[01:02:52] did a controlled comparison between
[01:02:54] using text skills and code skills. This
[01:02:56] was on a set of tasks which did have
[01:02:59] sort of more repeated structure. Um but
[01:03:02] we found that uh in comparison to no
[01:03:04] memory text skills um helped but code
[01:03:06] skills helped even more in terms of you
[01:03:09] know the accuracy of the system but also
[01:03:11] we got pretty big improvements in
[01:03:13] efficiency the number of times that the
[01:03:21] Cool.
[01:03:23] So, as we've kind of talked about
[01:03:25] before, a big potential issue with
[01:03:27] skills is that they might not be
[01:03:29] general. And here's a failure case of
[01:03:31] this approach and actually a failure
[01:03:33] case of these code skills. So, we tried
[01:03:35] to see how well could skills generalize
[01:03:39] across websites. And we induced um these
[01:03:41] code skills on one site uh and then we
[01:03:43] tried to apply them on a real website uh
[01:03:46] like the Target shopping site. So this
[01:03:48] skill um that was induced on a different
[01:03:51] site worked on that site but like um
[01:03:55] uses assumes that this uh this um
[01:03:56] particular element that you're
[01:03:59] interacting with has a drop down like
[01:04:01] this. Whereas on the target site it's
[01:04:04] you know this set of radio buttons and
[01:04:07] so it it fails there. And um you have to
[01:04:09] have the model be able to like actually
[01:04:12] edit the skill based on um feedback from
[01:04:14] the environment as it's interacting with
[01:04:23] But code has a solution to this, right?
[01:04:27] Uh so we have um abstract classes and
[01:04:29] those can be instantiated in different
[01:04:32] ways. There's this uh paper called poly
[01:04:35] skill which does this. So um they're
[01:04:37] using code as the representation sort of
[01:04:40] building on this ASI work that we did.
[01:04:42] Um, but the first time that the model
[01:04:44] interacts with a new website, it writes
[01:04:46] an abstract class which doesn't have
[01:04:49] implementations for the methods, but
[01:04:51] could have stubs like searching for a
[01:04:53] product, adding to a cart, checking out.
[01:04:57] And um, then it'll also write a website
[01:04:58] specific implementation of it like this
[01:05:00] one for Amazon. Then when it's
[01:05:02] interacting with a different site, you
[01:05:04] could have some metadata or you could
[01:05:05] even just have the language model
[01:05:08] trigger that this particular concrete
[01:05:10] implementation no longer applies. and
[01:05:11] then you'll write a different
[01:05:13] instantiation of the abstract class. And
[01:05:15] they show that this helps too. Um, this
[01:05:17] is also nice because it gives you a way
[01:05:19] to have like a large number of specific
[01:05:23] skills, but only have a subset of them
[01:05:25] be active at a given time that are
[01:05:26] actually relevant. So, this kind of
[01:05:28] makes sense, right? It's, you know, just
[01:05:29] a software engineering best practice
[01:05:38] Okay. Uh, yeah, we talked about all this
[01:05:40] already. um you guys had a good sense of
[01:05:42] the the pros and cons of each of these
[01:05:44] types of representation, but it's
[01:05:45] helpful to know that, you know, the
[01:05:47] skills standard allows you to combine
[01:05:50] both and um there's a lot of research to
[01:05:52] be done on the best way to combine these
[01:05:54] representations together. Um like uh
[01:05:56] said,
[01:05:59] okay, so we'll go quickly through a few
[01:06:01] papers um on different kind of like
[01:06:04] parts of this skill life cycle. This is
[01:06:06] a really open research topic of like
[01:06:08] what are the best ways to induce and
[01:06:11] manage these skills. Um you'll have the
[01:06:13] papers for for more details. Um but you
[01:06:16] can also explore this in your projects
[01:06:17] uh towards the end of the lecture or the
[01:06:22] end of the class if you're interested.
[01:06:23] Everything we've talked about so far has
[01:06:26] been learning from success, but it's
[01:06:28] also potentially pretty helpful to learn
[01:06:31] from failures. So say that the model
[01:06:33] like tries to carry out this task like
[01:06:35] um you know searching for Bluetooth
[01:06:38] headphones. Um but for this particular
[01:06:40] website they sort of have like their
[01:06:43] search terms are or rather than and so
[01:06:45] you get a list of everything that's
[01:06:47] Bluetooth or headphones or a Sony. This
[01:06:49] is a real example from this reasoning
[01:06:51] bench paper from Google. So you get like
[01:06:54] 5,000 results and the agent just breaks
[01:06:57] on this like it has to pagionate through
[01:06:59] all of these 5,000 results. it does, you
[01:07:02] know, it loses track of what the task is
[01:07:06] and it fails. But if we observe that um
[01:07:08] failed trajectory sort of in the
[01:07:11] reflection style way, we could uh
[01:07:13] produce some text that gives guidance on
[01:07:15] how to avoid it in the future. Like
[01:07:17] saying um we should give a more specific
[01:07:18] search term rather than this more
[01:07:21] general one and we should you know have
[01:07:23] like a larger number of items displayed
[01:07:25] so the model gets more in its context
[01:07:28] window at once. And this paper um
[01:07:30] generally uses the same framework as
[01:07:33] like uh agent workflow memory, agent
[01:07:34] skill induction, but instead of just
[01:07:36] having these kind of abstractions of the
[01:07:39] correct trajectories, it generates this
[01:07:42] text feedback um which um is applicable
[01:07:45] to failed trajectories too and is also
[01:07:46] you know the kind of thing that you
[01:07:49] would write in a skill yourself um if
[01:07:52] you were writing one
[01:07:53] and they find that this is pretty
[01:07:55] helpful. So these are different like
[01:07:58] types of memory. Um so synapse uses
[01:07:59] trajectories
[01:08:01] like full trajectories with all of the
[01:08:04] actions and observations all the tool
[01:08:06] calls and messages. Um this is agent
[01:08:08] workflow memory that uses these slightly
[01:08:11] abstracted parts of trajectories. And
[01:08:14] this is their approach that uses these
[01:08:17] text descriptions of strategies and um
[01:08:19] adding and negatives going you know
[01:08:21] adding and negative examples as inputs
[01:08:25] to the memory. um uh doesn't improve
[01:08:27] performance when you're using either
[01:08:30] trajectories or
[01:08:33] um workflows, but does improve
[01:08:34] substantially when you have sort of
[01:08:36] these text descriptions, which kind of
[01:08:38] makes sense given the example we saw
[01:08:40] before because you can describe in a
[01:08:43] general way how not to fail
[01:08:45] rather than remembering and conditioning
[01:08:52] Another important thing to think about
[01:08:55] is we're deciding whether to store
[01:08:58] trajectories um you know store things in
[01:09:01] the memory or what type of strategies to
[01:09:04] infer from the examples based on whether
[01:09:06] we judged the example to be successful
[01:09:10] or not. That's in most of this work
[01:09:12] using a model as a judge that looks at
[01:09:14] the final state of the trajectory, looks
[01:09:16] at the task that you were trying to
[01:09:18] solve and predicts does it seem like I
[01:09:20] got it correct or not. So a really good
[01:09:23] question to ask here is what you know
[01:09:27] how much does the quality of that judge
[01:09:29] affect the performance of the algorithm
[01:09:30] because we know the judges aren't
[01:09:33] perfect. Um this paper reasoning bank
[01:09:36] controlled for this. So they um run
[01:09:39] their methods with a perfect judge. Um
[01:09:43] and they also like to so they use kind
[01:09:44] of the ground truth knowledge of whether
[01:09:47] it succeeded or not. Um but then they
[01:09:49] add some noise into that and so you're
[01:09:53] able to control um the accuracy the
[01:09:55] simulated accuracy of judging this
[01:09:58] trajectory and the performance does fall
[01:09:59] off but they find there's kind of a
[01:10:03] sweet spot where um you do get
[01:10:06] improvements from the memory um and uh
[01:10:08] there's sort of a widish range of
[01:10:11] accuracies where using the judge to
[01:10:13] induce the memory is helpful but there's
[01:10:22] Okay. And uh yeah, with the last few
[01:10:26] minutes, um I want to come back to we
[01:10:28] had a question before about does having
[01:10:31] more skills than are necessary um
[01:10:33] potentially hurt performance? And we
[01:10:36] also had a question about like um we're
[01:10:40] if we're retrieving skills from a set um
[01:10:42] does that retriever matter? Like does
[01:10:45] the quality of that retriever matter? So
[01:10:46] um there were some nice ablation
[01:10:49] experiments in this reasoning bank paper
[01:10:53] that uh control um how many experiences
[01:10:56] you are retrieving from the memory that
[01:10:59] you have and they show that performance
[01:11:02] does fall out fall off as you have more
[01:11:05] available. Um so this could be because
[01:11:09] of a couple different factors. So um you
[01:11:11] know maybe you just haven't run your
[01:11:14] agent on that many tasks and maybe
[01:11:17] there's nothing relevant in your memory.
[01:11:20] So putting more stuff in is just bound
[01:11:22] to be irrelevant. That would be sort of
[01:11:24] like just a fundamental limitation of
[01:11:26] this approach applied in that setting.
[01:11:28] Right? You can only learn if there's
[01:11:31] some similarities between the things
[01:11:32] you're learning from and the things
[01:11:34] you're applying to. But it could also be
[01:11:37] like a limitation of the model itself.
[01:11:39] Maybe the model gets thrown off by
[01:11:41] having more things available in the
[01:11:43] context window. That could potentially
[01:11:45] be fixed by training the model, right?
[01:11:47] To be better at not being distracted by
[01:11:49] irrelevant context, to be better at
[01:11:51] reasoning about what's actually
[01:11:59] And um yeah, it can also potentially be
[01:12:02] useful to uh explicitly reduce the size
[01:12:05] of your memory um so that there's less
[01:12:08] of a burden on the language model to
[01:12:10] select from the things that are in it.
[01:12:13] And um we did some work on this that
[01:12:15] sort of uses like a caching type
[01:12:17] approach um that you just look and see
[01:12:19] how often has a particular item in your
[01:12:22] memory been used in the past um and if
[01:12:24] it hasn't been used very frequently,
[01:12:26] you'll drop it.
[01:12:28] And this can you know improve this
[01:12:31] efficiency of the approaches quite a bit
[01:12:33] because you don't have to put as much in
[01:12:35] your context window but can also improve
[01:12:36] their success if the models are getting
[01:12:38] distracted by things that are
[01:12:43] Yeah. And the very last thing that we'll
[01:12:46] cover is so all of this was in some ways
[01:12:48] a little bit ad hoc, right? Like we were
[01:12:50] just having the language model look at
[01:12:53] these past experiences and then produce
[01:12:55] a skill which would be put in the memory
[01:12:58] and used in the future. But we're just
[01:13:00] like prompting the language model to
[01:13:02] predict things that seem like they might
[01:13:04] be useful in the future. And a really
[01:13:06] natural question is could you just train
[01:13:08] the language model to do that directly?
[01:13:11] Um you can. Um this is a direction
[01:13:12] that's starting to be explored just
[01:13:15] really recently. So these papers um are
[01:13:17] just appearing at you know just appeared
[01:13:21] at ACL um this year. But the basic idea
[01:13:22] here is that we're going to do
[01:13:25] reinforcement learning over multiple
[01:13:27] tasks seen in sequence. So this online
[01:13:29] learning setting that we've been
[01:13:31] covering for evaluation, we're also
[01:13:33] going to run training on it. We'll get
[01:13:36] multiple similar tasks in sequence and
[01:13:40] we'll be building up the memory. um in
[01:13:41] the same way that we've been doing
[01:13:43] before by inducing skills from the
[01:13:45] experience and using the memory on the
[01:13:49] future tasks. So this is a very complex,
[01:13:50] you know, process, right? Like we're
[01:13:53] using a couple different models here. Uh
[01:13:55] we're storing things in a memory. We're
[01:13:57] retrieving those. We're using them. But
[01:13:59] the good thing is reinforcement learning
[01:14:00] doesn't care. You can just apply
[01:14:02] reinforcement learning to complex
[01:14:04] non-ifferiable processes like this.
[01:14:06] We'll have a couple lectures that show
[01:14:11] you how. Um and you can get reward from
[01:14:12] uh
[01:14:17] did this second task succeed and did it
[01:14:20] use tasks that were induced in the past.
[01:14:21] So you can just do reinforcement
[01:14:25] learning on this reward being trained on
[01:14:27] um skill induction on sequences of
[01:14:31] similar tasks. And um there's a couple
[01:14:32] papers that have explored this. They
[01:14:35] both find that this is helpful. And uh
[01:14:36] one of them had this interesting result
[01:14:40] that um it helps to improve success if
[01:14:42] you also include this reward term that
[01:14:45] incentivizes reuse of the skills. So you
[01:14:47] could also imagine like introducing
[01:14:49] other sorts of reward terms that like
[01:14:51] minimize the size of the skill libraries
[01:14:53] that you've induced to try to you know
[01:14:56] kind of keep things regularized and not
[01:14:58] overfit too much. Um I think there's a
[01:14:59] lot of interesting like feature work
[01:15:03] that could be explored here.
[01:15:06] And um yeah that's uh that's all the
[01:15:09] time that we have. Uh but uh hopefully
[01:15:11] you got a sense for the way that skills
[01:15:14] are induced and also written. Um you'll
[01:15:15] apply those in your projects and you can
[01:15:17] explore them in the research projects
[01:15:19] too. I'll stick around for a few minutes
