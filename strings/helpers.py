ABOUT_BOT = """
Meet <b>Alphabot</b>, a powerful music + group management bot packed with magical features. 🧙‍♂️✨  
From seamless music playback to intelligent spam control, Harry is your all-in-one assistant for Telegram groups and channels.

<b>🔧 Powered By:</b>  
Built with love and precision by <a href="https://t.me/devforgekush">@devforgekush</a> — ensuring quality, stability, and performance.  
Operates under the GNU General Public License v3.0 🛡️

<b>🧩 Core Features:</b>  
• 🎧 High-quality music playback in voice/video chats  
• 🚫 Anti-spam & smart filters  
• 👋 Auto Welcome & Goodbye messages  
• 🧞 AFK, bio link scanning, and media controls  
• 🖼️ Video thumbnails, song info, and more  
• ⚙️ Fully customizable admin tools and auto-moderation

<b>💬 Need help?</b>  
Hop into the Hogwarts Help Desk at <a href="https://t.me/devforgekush">Support Chat</a> — we're always here to assist! 🔮
"""

HELP_1 = """
<b>💤 AFK SYSTEM</b>

Let users know when you're away from keyboard (AFK).  
AFK status will be auto-removed when you're active again.

<b>🧩 Command:</b>
• <code>/afk</code> — Set AFK without a reason  
• <code>/afk [reason]</code> — Set AFK with a custom reason  
• <code>/afk [reason]</code> (as reply to photo/video/sticker) — Set media-based AFK  

Once you're back, the bot auto-removes AFK and notifies others.  
It also notifies when someone tries to mention or reply to an AFK user.

<b>🌟 Stay invisible when you're busy. Let your silence speak.</b>
"""

HELP_2 = """
<b>🎌 ANIME & MANGA EXPLORER</b>

Dive into the world of Anime, Manga & Characters.  
Fetch details, airing schedules, genres, and more instantly.

<b>🧩 Commands:</b>
• 🌀 <code>/anime [name]</code> — Get info about an anime  
• 📚 <code>/manga [name]</code> — Get manga details  
• 👤 <code>/character [name]</code> — Info about any character  
• 🏷️ <code>/gettags</code> — Explore available genre tags  
• 🔍 <code>/browse</code> — Browse trending / upcoming / latest anime  
• ⚙️ <code>/anisettings</code> — AniList bot settings  
• 📺 <code>/airing [anime]</code> — Shows upcoming airing schedule  
• 🏆 <code>/topanime</code> — Lists top anime rankings

<b>🌟 Discover your next obsession in the anime universe!</b>
"""

HELP_3 = """
<b>📢 ANNOUNCEMENT SYSTEM</b>

Enable and manage announcement messages in your group.  
Useful for anime episode alerts or any broadcast messages.

<b>🧩 Command:</b>
• 📢 <code>/announcement</code> — Enable or disable announcements in the current chat

<b>💡 Perfect for keeping your community updated!</b>
"""

HELP_4 = """
<b>🚫 ANTI-CHANNEL SYSTEM</b>

Prevent users with channel-linked profiles from interacting in your group.  
Automatically removes such users when enabled.

<b>🧩 Command:</b>
• 🚫 <code>/antichannel</code> — Enable or disable anti-channel protection

<b>🔒 Keep your group safe from bot channels and spammy profiles!</b>
"""

HELP_5 = """
<b>🛡️ ANTI-BANALL PROTECTION</b>

🛑 Protect your group from rogue admins misusing mass ban powers.  
🧠 When enabled, it keeps an eye on bulk ban activity and responds instantly.

<b>🧩 Command:</b>
• 🚷 <code>/antibanall</code> — Toggle anti-banall protection in your group

<b>🔁 What It Does:</b>
• 🧮 If any admin bans more than 5 users within 10 seconds:  
   ┗ ❌ They will be automatically demoted (if I have rights)  
   ┗ 📢 If not, all admins will be alerted about the abuse attempt

<b>⚠️ Keep your community safe from rogue moderation!</b>
"""

HELP_6 = """
<b>✅ USER APPROVAL SYSTEM</b>

Grant special permissions to trusted users, exempting them from restrictions like antiflood, locks, and blacklists.

<b>🧩 Commands:</b>
• <code>/approval</code> — Check a user's approval status in this chat  
• <code>/approve</code> — Approve a user (removes locks & blacklist effects)  
• <code>/unapprove</code> — Remove approval from a user  
• <code>/approved</code> — List all currently approved users  
• <code>/unapproveall</code> — Unapprove <b>ALL</b> users in the chat (⚠️ irreversible)

<b>🧪 Example:</b>  
• <code>/approve @username</code> — Approves a user in the current chat

<b>🔐 Use wisely to manage exemptions efficiently!</b>
"""

HELP_7 = """
<b>🌐 SEARCH MODULE</b>

🔍 Search Google or StackOverflow directly from your Telegram group!  
⚡ Instantly fetch results and browse with one tap.

<b>🧩 Commands:</b>
• 🔎 <code>/google [query]</code> — Search Google for any topic  
• 💻 <code>/stack [query]</code> — Search StackOverflow for programming help

<b>🔁 What It Does:</b>
• 📄 Returns top 5 search results with direct links  
   ┗ 🧠 Helpful for developers, admins, and curious users  
   ┗ 📌 All results are clickable and open in browser

<b>⚠️ Perfect tool to answer questions instantly without leaving Telegram!</b>
"""

HELP_8 = """
<b>🛡️ MODERATION COMMANDS</b>

🚨 Instantly moderate your group with powerful tools like banning, muting, and unmuting users — all via simple commands.

<b>🧩 Commands:</b>
• 🚫 <code>/ban</code> — Ban a user permanently  
• ♻️ <code>/unban</code> — Revoke a user's ban  
• 🔇 <code>/mute</code> — Mute a user indefinitely  
• 🔊 <code>/unmute</code> — Unmute a muted user  
• ⏱️ <code>/tmute</code> — Temporarily mute users  
   ┗ <code>2m</code> = 2 minutes | <code>1h</code> = 1 hour | <code>3d</code> = 3 days

<b>💡 How It Works:</b>
• 🧾 Works by replying to a message or tagging a user  
• 📌 Accepts optional reasons for logging purposes  
• ⚠️ Only works if you (and the bot) have proper admin permissions

<b>👮 Great for managing spammers and keeping the chat clean!</b>
"""

HELP_9 = """
<b>🚫 BLACKLIST CHAT MODULE</b>

🔒 Restrict the bot from working in unwanted groups by blacklisting them.  
✅ You can also remove them from blacklist later.

<b>🧩 Commands:</b>
• 🧨 <code>/blchat &lt;chat_id&gt;</code> — Blacklist a group and force bot to leave  
• 🎯 <code>/unblchat &lt;chat_id&gt;</code> — Whitelist the group again  
• 📜 <code>/blchats</code> — View all currently blacklisted group chats

<b>🔁 What It Does:</b>
• 🚷 Prevents the bot from being used in blacklisted groups  
• 💣 Bot will automatically leave the group upon blacklisting  
• ⚙️ Only SUDO users can use these commands

<b>⚠️ Useful for handling abuse or blocking unwanted access!</b>
"""

HELP_10 = """
<b>🧮 CALCULATOR MODULE</b>

🧠 Perform instant mathematical calculations with ease using this module.

<b>🧩 Commands:</b>
• ➕ <code>/calculate &lt;expression&gt;</code> — Evaluate a full math expression  
• 🔢 <code>/calc &lt;expression&gt;</code> — Shortcut for /calculate

<b>📌 Examples:</b>
• 🧾 <code>/calculate 2 + 2</code>  
• 📐 <code>/calc (5 + 3) * 2</code>  
• 🌐 <code>/calc sin(30)</code>  
• 🧊 <code>/calc sqrt(16)</code>

<b>⚠️ Supports basic arithmetic, trigonometry, square roots, and more!</b>
"""

HELP_11 = """
<b>🧹 SERVICE CLEANER MODULE</b>

♻️ Automatically clean up clutter from your chat.

<b>🛠️ Command:</b>
• ✧ <code>/cleaner</code> — Toggle the service cleaner status in the chat.

<b>✨ What It Does:</b>
• 🗑️ Deletes system-generated service messages (e.g., user joined/left).  
• 🚫 Also removes messages starting with command prefixes automatically.

<b>💡 Usage:</b>
• Use <code>/cleaner</code> to enable or disable this auto-cleaning feature anytime.
"""

HELP_12 = """
<b>🎭 Cosplay Command</b>

✨ Get a random cosplay image from the internet with a simple command!

<b>🧩 Command:</b>
• 🤖 <code>/cosplay</code> — Fetch a random cosplay image

<b>⚙️ What It Does:</b>
• 📷 Returns a random cosplay image from a database
• 💬 Includes a support button for inquiries
• ✖ Close button to dismiss the image

<b>🎉 Enjoy your cosplay for today!</b>
"""

HELP_13 = """
<b>💞 Couple of the Day</b>

Pair up two random users in your group as the couple of the day!  
Fun and engaging for active communities.

<b>🧩 Command:</b>
• 🤖 <code>/couples</code> — Select a random couple from the group

<b>💡 What It Does:</b>
• 💘 Picks 2 random non-bot members from the group  
• 💌 Displays them as a couple with today’s date  
• 🔁 Updates daily — encourages daily interaction  
• ✖️ Includes a “Close” button and Support link

<b>⚠️ Note:</b>
• Only works in groups
• Skips bots and repeats

<b>🎉 A perfect feature to keep the vibe alive!</b>
"""

HELP_14 = """
<b>💱 Currency Converter</b>

Convert between different global currencies right within your chat!

<b>🧩 Commands:</b>
• 💰 <code>/currency [amount] [from] [to]</code> — Convert an amount from one currency to another  
• 🌍 <code>/currency list</code> — Show all supported currency codes

<b>💡 Examples:</b>
• 💵 <code>/currency 100 USD EUR</code> → Convert 100 US Dollars to Euros  
• 💴 <code>/currency 50 JPY INR</code> → Convert 50 Japanese Yen to Indian Rupees

<b>⚙️ What It Does:</b>
• 🔄 Fetches real-time exchange rates  
• 📊 Works with over 150 currencies  
• 📌 Auto-validates input for accurate results

<b>✅ Tip:</b>
Use ISO currency codes (e.g., USD, INR, EUR)

<b>💡 Stay updated with global values anytime!</b>
"""

HELP_15 = """
<b>🎬 Video Downloader</b>

Download videos from YouTube, Instagram, and many other platforms — directly into your chat!

<b>🧩 Command:</b>
• 📥 <code>/video [link or query]</code> — Download a video by providing a direct link or search term

<b>💡 What It Does:</b>
• 🔗 Accepts links from YouTube, Instagram, Facebook, and more  
• 🔍 If no link is provided, performs a YouTube search  
• 🎞️ Downloads the video and uploads with full metadata (title, duration, etc.)

<b>⚙️ Usage:</b>
• 1️⃣ Use <code>/video</code> followed by a valid video link or keyword  
• 2️⃣ Bot fetches, processes, and delivers the video directly

<b>🚫 Note:</b>
• Some platforms may block access to private or region-locked content  
• Videos may take longer depending on size and platform

<b>📽️ One command to fetch any video you need — fast, easy, and reliable!</b>
"""

HELP_16 = """
<b>🗜️ Zip / Unzip Files</b>

Easily compress and extract files right inside Telegram. Perfect for sharing or organizing documents.

<b>🧩 Commands:</b>
• 🧩 <code>/zip</code> — Compress any replied document into a .zip file  
• 📂 <code>/unzip</code> — Extract all contents from a replied .zip file

<b>💡 What It Does:</b>
• 📦 Zips any single file and sends it back  
• 📤 Unzips a .zip file and sends each file extracted  
• 🧹 Automatically removes temporary files to save space

<b>⚠️ Note:</b>
• You must reply to a document when using these commands  
• For unzip, only works on valid `.zip` files  
• Handles file I/O safely with cleanup after each operation

<b>📁 Fast & simple file management at your fingertips!</b>
"""

HELP_17 = """
<b>🧰 Extras Toolkit</b>

A collection of fun, utility, and helper tools to boost engagement and provide quick access to unique features.

<b>🧩 Commands:</b>
• 🎯 <code>/pickwinner</code> — Randomly selects a winner from a list  
• 🔁 <code>/echo</code> — Repeats back any text you provide  
• 🌐 <code>/webss [URL]</code> — Takes a live screenshot of the given webpage  
• 📖 <code>/ud [word]</code> — Searches the Urban Dictionary for slang or fun definitions

<b>💡 What It Does:</b>
• 🎉 Great for giveaways, fun polls, and text repetition  
• 🖼️ Instantly captures snapshots of websites for previews  
• 🧠 Explores internet slang or trending definitions quickly

<b>⚙️ Usage:</b>
• Use commands as-is or with necessary parameters  
• Ideal for casual groups, contests, and daily utility

<b>✨ Make your chats smarter, livelier, and more interactive with these handy tools!</b>
"""

HELP_18 = """
<b>🧹 Chat Filters</b>

Automatically respond to specific keywords in your group using custom triggers.

<b>🧩 Commands:</b>
• ➕ <code>/filter [keyword]</code> (reply) — Create a filter with the replied content  
• 📃 <code>/filters</code> — List all active filters in the current chat  
• ❌ <code>/stopfilter [keyword]</code> — Delete a specific filter by name  
• 🚫 <code>/stopall</code> — Delete all filters (only by group owner)

<b>💡 What It Does:</b>
• 🧠 Remembers a keyword and sends your saved message whenever someone mentions it  
• 📥 Filters can include text, media, buttons, etc.  
• 🔐 Only admins can create/remove filters (unless locked)

<b>⚙️ Usage:</b>
• 1️⃣ Reply to any message and send <code>/filter hello</code> — now "hello" triggers it  
• 2️⃣ Use <code>/filters</code> to view all filters  
• 3️⃣ Use <code>/stopfilter hello</code> to remove one, or <code>/stopall</code> to wipe them all

<b>⚠️ Notes:</b>
• Only the group owner can use <code>/stopall</code>  
• Filter matches are case-insensitive and keyword-based

<b>🔁 Smart automation for repetitive responses — set and forget!</b>
"""

HELP_19 = """
<b>🔤 Font Styler</b>

Turn your plain text into stylish fonts using various effects and Unicode styles.

<b>🧩 Command:</b>
• 🎨 <code>/font [text]</code> or <code>/fonts [text]</code> — Show buttons to convert your text into multiple cool font styles

<b>💡 What It Does:</b>
• ✨ Applies a variety of font transformations like serif, script, gothic, bubble, etc.  
• ⌨️ Sends the stylized version of your input text  
• 🧠 Over 40 unique fonts in a single interface!

<b>⚙️ Usage:</b>
• 1️⃣ Use <code>/fonts your text here</code>  
• 2️⃣ Choose a font from the button options  
• 3️⃣ Get your text instantly converted and ready to copy or forward

<b>📚 Examples:</b>
• <code>/fonts hello world</code>  
• Choose 𝙏𝙮𝙥𝙚𝙬𝙧𝙞𝙩𝙚𝙧 → Get: <code>𝙝𝙚𝙡𝙡𝙤 𝙬𝙤𝙧𝙡𝙙</code>

<b>🎯 Over 40 Fonts Supported:</b>
• Typewriter, Serif, Script, Comic, Tiny, Gothic, Bubble, Clouds, Circles, Slash, Strike, and many more...

<b>🖋 Express your text with style — make your messages stand out!</b>
"""

HELP_20 = """
<b>🎲 Fun Emoji Games</b>

Play interactive games using Telegram's animated dice emojis — have fun with your friends in chat!

<b>🧩 Commands:</b>
• 🎲 <code>/dice</code> — Roll a classic dice  
• 🎯 <code>/dart</code> — Hit the dart board  
• 🏀 <code>/basket</code> — Shoot a basketball  
• 🎳 <code>/ball</code> — Knock down bowling pins  
• ⚽ <code>/football</code> — Score a goal  
• 🎰 <code>/jackpot</code> — Spin a slot machine

<b>💡 What It Does:</b>
• Sends a fun animated emoji with random results  
• Replies with your name and the score/landing result  
• Great for friendly challenges and group fun!

<b>📚 Example:</b>
• <code>/dart</code> → 🎯 lands on 6 → Reply: "Hey Alice, your Score is: 6"

<b>🕹 Game On — Try your luck and challenge your friends!</b>
"""

HELP_21 = """
<b>👋 Welcome Greetings</b>

Automatically greets new members in your group with a customizable welcome message.

<b>🧩 Command:</b>
• ✅ <code>/welcome on</code> — Enable welcome greetings  
• 🚫 <code>/welcome off</code> — Disable welcome greetings  

<b>💡 Features:</b>
• 🎉 Sends welcome message when new user joins  
• ✍️ Editable template support (coming soon)  
• 📎 Media welcome (in future updates)  

<b>⚙️ Usage:</b>
• Just type <code>/welcome on</code> to activate greetings  
• Type <code>/welcome off</code> to stop sending messages  
• Set custom messages (optional future feature)  

<b>📚 Example:</b>
<code>/welcome on</code>  
<code>/welcome off</code>

<b>ℹ️ Default:</b> Welcome feature is <b>enabled by default</b> in all groups.

<b>🔐 Keep your group friendly and engaging with automated greetings!</b>
"""

HELP_22 = """
<b>🛠 Group Management Tools</b>

Powerful tools to manage group settings, pins, and appearance with ease.

<b>🧩 Commands:</b>

• 📌 <code>/pin</code> — Reply to a message to pin it in the group  
• 🔓 <code>/unpin</code> — Reply to a pinned message to unpin it  
• 📍 <code>/pinned</code> — View the latest pinned message  
• 🖼 <code>/setphoto</code> — Reply to a photo to set it as group profile picture  
• 🧹 <code>/removephoto</code> — Remove the group photo  
• 📝 <code>/settitle [text]</code> — Change group title (or reply with text)  
• 💬 <code>/setdescription [text]</code> — Set group description (or reply with text)  
• 🚪 <code>/lg</code> — Force bot to leave the group (owner only)

<b>🔐 Permissions Required:</b>
• Pin Messages, Change Group Info depending on the command  
• Bot must be admin with sufficient rights  

<b>📚 Examples:</b>
• <code>/pin</code> (as a reply)  
• <code>/settitle My New Group</code>  
• <code>/setdescription Welcome to our awesome community!</code>

<b>🔧 Manage your Telegram group like a pro!</b>
"""

HELP_23 = """
<b>🆔 ID Identifier</b>

Instantly fetch IDs of users, chats, replies, and even forwarded or sender chats — all in one powerful command.

<b>🧩 Command:</b>
• 🆔 <code>/id</code> — Shows your ID, chat ID, and message ID  
• 🔍 <code>/id @username</code> — Get ID of a specific user by mention  
• 📥 <i>Reply to any message and run</i> <code>/id</code> — Get replied user's ID and more

<b>💡 What It Detects:</b>
• 🧾 Message ID  
• 👤 Your User ID  
• 💬 Current Chat ID  
• ↩️ Replied User ID & Mention  
• 📢 Forwarded Channel or Sender Chat ID  
• 🙋 Queried Username or ID

<b>⚙️ Usage:</b>
• 1️⃣ Type <code>/id</code>  
• 2️⃣ Or reply to a user or message  
• 3️⃣ Or use <code>/id @username</code>  
• ✅ Bot will fetch all relevant IDs and show them with a Close button

<b>📚 Examples:</b>
• <code>/id</code>  
• <code>/id @devforgekush</code>  
• <i>Reply to a forwarded message and use</i> <code>/id</code>

<b>🔐 Use it to debug, verify admins, track users or for logs — all in seconds!</b>
"""

HELP_24 = """
<b>🌀 Imposter Mode</b>

Detect users who frequently change their name, username, or profile — useful for identifying spammers or impersonators.

<b>🧩 Commands:</b>
• 🟢 <code>/imposter enable</code> — Start monitoring name or username changes in the group  
• 🔴 <code>/imposter disable</code> — Stop imposter detection in the group  
• 👁️ <code>/imposter status</code> — Check current imposter monitoring status  
• 📛 <code>/imposter reset</code> — Reset the entire imposter cache for the group

<b>💡 What It Does:</b>
• 🧠 Tracks users who frequently change name, last name, or username  
• 🚨 Sends a warning message when a suspicious change is detected  
• 🔒 Helps admins moderate impersonation and spam activities

<b>⚙️ Usage:</b>
• 1️⃣ Admin uses <code>/imposter enable</code>  
• 2️⃣ Bot logs and compares user profile data silently  
• 3️⃣ On suspicious change, it alerts the group with context

<b>📌 Note:</b>
• Only admins can toggle or reset imposter tracking  
• OWNER_ID is always ignored in tracking

<b>🛡 Stop impersonators before they strike — with smart identity tracking!</b>
"""

HELP_25 = """
<b>📥 Instagram Media Downloader</b>

Easily download Instagram reels, videos, and image posts directly into your chat.

<b>🧩 Command:</b>
• 🔗 <code>/ig [url]</code> or <code>/instagram [url]</code> or <code>/reel [url]</code> — Download any public Instagram media

<b>💡 What It Does:</b>
• 📸 Downloads reels, videos, and images from the given Instagram link  
• 🎞 Detects content type and sends the file accordingly (video, photo, or document)  
• 🔘 Includes a button to open the original Instagram post

<b>⚙️ Usage:</b>
• 1️⃣ Copy any public Instagram post/reel URL  
• 2️⃣ Use <code>/ig [paste link here]</code>  
• 3️⃣ Bot will fetch and send the media with a button to view it on Instagram

<b>📚 Examples:</b>
• <code>/ig https://www.instagram.com/reel/Cxyz123/</code>  
• <code>/reel https://www.instagram.com/p/Cabc456/</code>

<b>⚠️ Note:</b>
• Only works for **public** Instagram posts (reels, videos, photos)  
• Private or deleted posts cannot be downloaded  
• Bot must have permission to send media in the chat

<b>🚀 Save your favorite Instagram content with one simple command!</b>
"""

HELP_26 = """
<b>🔓 AUTO-APPROVE JOIN REQUESTS</b>

👥 Instantly approve users who request to join your group without manual approval.  
🎉 Sends them a welcome message with a quick close button.

<b>🧩 Command:</b>
• 🤖 <code>/autojoin</code> — Toggle auto-approval of join requests in your group

<b>🔁 What It Does:</b>
• ✅ Approves all incoming join requests automatically  
   ┗ 💌 Sends a custom welcome message with group name  
   ┗ ❌ Includes a “Close” button to dismiss the message

<b>⚠️ Useful for public groups or when overwhelmed with join requests!</b>
"""

HELP_27 = """
<b>🔐 Group Lock System</b>

Manage and secure your group by locking specific content types and permissions.

<b>🧩 Commands:</b>

• 🔒 <code>/lock [type]</code> — Lock a specific permission or content type  
• 🔓 <code>/unlock [type]</code> — Unlock a specific permission or content type  
• 🛡 <code>/locks</code> — View current locked permissions in the group  
• 📋 <code>/locktypes</code> — List all available lock types you can use

<b>📚 Examples:</b>
• <code>/lock media</code> — Restricts users from sending any media  
• <code>/lock links</code> — Prevents sending links in chat  
• <code>/unlock stickers</code> — Allows stickers again in the chat

<b>🧠 Available Lock Types Include:</b>
• Media, Stickers, Photos, Videos, Voice, Forward, Contact, GIFs, URLs, Bots, Games, Inline, Polls, and more

<b>⚙️ Usage Notes:</b>
• Only admins can lock/unlock  
• Locked items are instantly restricted from all users

<b>🔐 Use smart restrictions to keep your group clean and safe!</b>
"""

HELP_28 = """
<b>📑 Log Channel Management</b>

Track important group activities by setting up a dedicated log channel.

<b>🧩 Commands:</b>

• 🔗 <code>/setlog</code> — Link a log channel to your group  
• ❌ <code>/unsetlog</code> — Remove the current log channel  
• 📥 <code>/logchannel</code> — View the currently linked log channel

<b>📚 Examples:</b>
• <code>/setlog</code> — Forward a message from your log channel to the bot  
• <code>/unsetlog</code> — Stops logging group activity

<b>🧠 What It Logs:</b>
• Member joins and leaves  
• Message deletions and edits  
• Admin promotions/demotions  
• Bans, unbans, mutes, and other actions

<b>⚙️ Usage Notes:</b>
• The bot must be an admin in the log channel with permission to post  
• Only group admins can configure logging

<b>🔍 Stay informed with real-time group event logging!</b>
"""

HELP_29 = """
<b>🎨 Logo Generator</b>

Create stylish logos from text with various themes and effects.

<b>🧩 Commands:</b>

• 🖌️ <code>/logo [text]</code> — Generates a default styled logo  
• 🎨 <code>/clogo [text]</code> — Creates a custom-themed logo  
• 🖤 <code>/blogo [text]</code> — Generates a black & pink themed logo

<b>📚 Examples:</b>
• <code>/logo Yumeko</code> — Creates a basic Yumeko logo  
• <code>/clogo Custom Logo</code> — Generates logo with your custom style  
• <code>/blogo Blink Style</code> — Stylish black-pink themed output

<b>⚙️ Usage Notes:</b>
• Works in both private and group chats  
• Text input is required after the command

<b>🖼 Express yourself with unique, beautiful logos instantly!</b>
"""

HELP_30 = """
<b>👑 Owner Only Commands</b>

These commands can only be used by the bot owner in group chats.

<b>🔧 Available Commands:</b>

• 🚫 <code>/unbanall</code> — Unbans all banned users in the current group  
• 🔊 <code>/unmuteall</code> — Unmutes all muted users in the group  
• 🧟 <code>/zombies</code> — Bans all deleted (ghost) accounts in the group

<b>📌 Note:</b>
• These actions affect all users of the group  
• Use responsibly, as they may impact moderation history  
• Only works if you have proper admin rights

<b>⚠️ These are powerful tools — reserved for the supreme ruler (you).</b>
"""

HELP_31 = """
<b>🎵 Voice Chat Music Streaming</b>

This module provides a visual music streaming system for group voice chats using commands.

<b>🧑‍🎤 User Commands:</b>
• ▶️ <code>/play [song name]</code> — Start streaming the requested song  
• 🎥 <code>/vplay [video name]</code> — Start video streaming of the requested media  
• 🔁 <code>/forceplay [song name]</code> — Instantly replace current track with a new one  
• 📄 <code>/queue</code> — View the list of upcoming tracks  
• ♻️ <code>/restart</code> — Restart the music bot

<b>🛠 Admin Commands:</b>
• ⏭ <code>/skip</code> — Skip the currently playing track  
• ⏸ <code>/pause</code> — Pause the music stream  
• ▶️ <code>/resume</code> — Resume the paused music  
• ⏹ <code>/end</code> or <code>/stop</code> — Stop the music stream entirely  
• 🔄 <code>/reload</code> — Reload admin list in the bot

<b>🧑‍💻 Auth Users:</b>
Authorized users can access admin-level controls in the music module without being actual group admins.

• ✅ <code>/auth [username]</code> — Add a user to the bot's auth list  
• ❌ <code>/unauth [username]</code> — Remove a user from the auth list  
• 📋 <code>/authusers</code> — Show the list of all authorized users

<b>🎶 Let the music play — right inside your voice chat!</b>
"""

HELP_32 = """
<b>📰 News & Web Search Module</b>

This module allows users to search for news articles, images, and web results using Bing or other search sources.

<b>🔍 Available Commands:</b>

• 🗞 <code>/news [keyword]</code> — Search for recent news articles based on a keyword  
  <b>Example:</b> <code>/news football</code>

• 🔎 <code>/bing [query]</code> — Perform a Bing web search and get the top results  
  <b>Example:</b> <code>/bing Python programming</code>

• 🖼 <code>/img [query]</code> — Search for images related to your query  
  <b>Example:</b> <code>/img mountains</code>

<b>📌 Notes:</b>
• You can leave the keyword empty in <code>/news</code> to fetch trending general news  
• All results are fetched from reliable sources and displayed within the chat

<b>🌐 Stay informed, stay ahead — all within your Telegram group!</b>
"""

HELP_33 = """
<b>🌙 Night Mode System</b>

Automatically manage your group’s activity during night hours by restricting permissions.

<b>🧩 Commands:</b>

• 🌘 <code>/nightmode</code> — Open the night mode settings panel with options to enable/disable

<b>🕰 What it Does:</b>
• 🔒 Auto-locks the group every night at 12:00 AM IST  
• 🔓 Auto-unlocks the group every morning at 6:00 AM IST

<b>🧠 How it Works:</b>
• When enabled, the bot will restrict sending messages and media during night hours  
• Automatically restores permissions in the morning

<b>⚙️ Notes:</b>
• Only group admins can use /nightmode  
• Works best with properly configured admin rights for the bot  
• Ideal for study/work groups to avoid late-night spam

<b>🌙 Use Night Mode to keep your group peaceful while members rest!</b>
"""

HELP_34 = """
<b>🔲 QR Code Generator</b>

Easily generate a QR code from any text, link, or message using a simple command.

<b>🧩 Command:</b>

• <code>/qr [text]</code> — Generates a QR Code for the provided text or link

<b>📚 Examples:</b>
• <code>/qr https://example.com</code>  
• <code>/qr Alphabot is awesome</code>

<b>🧠 What It Does:</b>
• Converts your input into a clean QR image  
• Sends it back as a PNG image instantly

<b>⚙️ Usage Notes:</b>
• Works in both group and private chats  
• Useful for sharing links, messages, or IDs securely via QR

<b>🔲 Fast and simple QR generation with just one command!</b>
"""

HELP_35 = """
<b>🖼️ Quote Generator</b>

Create stylized quote stickers or images from any replied message.

<b>🧩 Command:</b>

• <code>/q</code> — Quote the replied message  
• <code>/q [count] [flags]</code> — Customize the quote with extra options

<b>📚 Examples:</b>
• <code>/q</code> — Quote the single replied message  
• <code>/q 3</code> — Quote 3 messages starting from the reply  
• <code>/q reply red png</code> — Quote with reply message, red background, in PNG  
• <code>/q 2 #123abc</code> — Quote 2 messages with custom hex color background

<b>🎨 Flags & Options:</b>
• <code>1-10</code> — Number of messages to quote (default is 1)  
• <code>reply</code> or <code>r</code> — Include replied message in the quote  
• <code>png</code> / <code>webp</code> — Output format (default: webp sticker)  
• Color options: red, blue, green, yellow, pink, black, white, etc.  
• Hex colors like <code>#ffcc00</code> are also supported  
• <code>random</code> — Choose a random background color

<b>⚙️ Usage Notes:</b>
• Only works by replying to a message  
• Avoid using on media messages (text only)  
• Output is sent as a sticker (webp) or image (png)

<b>🖼 Quote your favorite messages with style and flair!</b>
"""

HELP_36 = """
<b>🔎 Reverse Image Search</b>

Easily find the source of any anime, artwork, or media using powerful SauceNao engine.

<b>🧩 Commands:</b>

• ✧ <code>/reverse</code> — Search the source of a replied image  
• ✧ <code>/sauce</code> — Alternative command for reverse image lookup  
• ✧ <code>/pp</code> — Alias for quick SauceNao search

<b>📚 Usage Tips:</b>
• Make sure to reply to a photo, sticker, or document  
• Works best with anime artwork, digital art, or screenshots  
• Shows similarity %, title, and source link

<b>💡 Perfect tool to find anime scenes, artists, or original sources!</b>
"""

HELP_37 = """
<b>🧬 Generate Session Strings Easily</b>

Quickly create Pyrogram or Telethon sessions — for user or bot accounts.

<b>🧩 Main Command:</b>

• ✧ <code>/sgen</code> — Start session generator and choose between Pyrogram or Telethon (User/Bot modes)

<b>👤 Steps for User Sessions:</b>
1. Enter your <b>API_ID</b> and <b>API_HASH</b> (or use <code>/skip</code> to auto-fill defaults)  
2. Input your phone number in international format (e.g., <code>+1234567890</code>)  
3. Provide the OTP code sent by Telegram  
4. If prompted, enter your 2FA password

<b>🤖 Steps for Bot Sessions:</b>
1. Enter your <b>API_ID</b> and <b>API_HASH</b> (or <code>/skip</code> to use defaults)  
2. Provide your <b>bot token</b> (e.g., <code>123456:ABCdefGHI</code>)

<b>📤 Output:</b>
• Your session string will be saved to <b>Saved Messages</b> (for user sessions)  
• Displayed directly in chat (for bot sessions)

<b>🛠️ Extra Commands:</b>
• ✧ <code>/cancel</code> — Cancel the current session generation  
• ✧ <code>/skip</code> — Use default API ID and API HASH

<b>🔐 Use sessions securely. Never share your session string with anyone.</b>
"""

HELP_38 = """
<b>📜 Random Shayari</b>

Get beautifully crafted anime quotes and Hindi shayari on demand!

<b>🧩 Commands:</b>
• ✧ <code>/shayri</code> — Receive a random Hindi shayari

<b>📚 Usage Tips:</b>
• Shayari is suitable for romantic, sad, or deep vibes

<b>💡 Perfect for expression and aesthetic messages!</b>
"""

HELP_39 = """
<b>🏟️ Live Match Updates</b>

Get real-time updates for Cricket and Football matches with ease.

<b>🧩 Available Commands:</b>

• ✧ <code>/cricket</code> — View upcoming cricket match details  
• ✧ <code>/football</code> — View upcoming football match details

<b>🎮 Inline Navigation Features:</b>

• Use inline buttons to browse through live match info:
   ⏩ <b>Next Cricket Match</b>  
   ⏩ <b>Next Football Match</b>

<b>📌 Stay updated with your favorite sports instantly!</b>
"""

HELP_40 = """
<b>🧩 Sticker & Meme Tools</b>

Fun and powerful utilities for stickers, memes, and more!

<b>📜 Available Commands:</b>

• ✧ <code>/st &lt;sticker_id&gt;</code> — Send any sticker by file ID.  
• ✧ <code>/getsticker</code> — Extract a sticker image (reply to sticker).  
• ✧ <code>/kang</code> — Kang a replied image or sticker to your own pack.  
• ✧ <code>/packkang [pack name]</code> — Kang the entire replied sticker pack.  
• ✧ <code>/mmf top ; bottom</code> — Memeify an image with top and bottom text.

<b>📚 Usage Guide:</b>
• Use <code>/st</code> only with valid sticker IDs (starts with <code>CAAC...</code>).  
• <code>/getsticker</code> gives PNG or WEBP from replied sticker.  
• <code>/kang</code> auto adds to your first sticker pack.  
• <code>/packkang</code> copies the full pack and creates your version.  
• <code>/mmf</code> works on images or stickers — use semicolon <code>;</code> to split top/bottom text.

<b>💡 Create memes, share stickers, or make your own packs in seconds!</b>
"""

HELP_41 = """
<b>👥 Group Tagging System</b>

Mention all members in a group using customizable tag commands — perfect for calling everyone’s attention!

<b>📜 Available Commands:</b>

• ✧ <code>/tagall</code> — Tag all group members with a random message  
• ✧ <code>/spam</code>, <code>/tagmember</code>, <code>/utag</code>, <code>/stag</code>, <code>/hftag</code>, <code>/bstag</code>, <code>/eftag</code>, <code>/etag</code>, <code>/atag</code> — All are aliases of <code>/tagall</code>  
• ✧ <code>/tagoff</code> or <code>/tagstop</code> — Stop an ongoing tagging process

<b>🛠️ Features:</b>
• Sends friendly or funny tag lines with user mentions  
• Supports both direct commands and reply-based tagging  
• Prevents spamming by allowing only admins to use commands  
• Random emoji and rich messages to make tags more engaging  
• One tag per 4 seconds (anti-spam mechanism)

<b>🔒 Admin Only Commands</b>
Only admins or group owners can initiate or stop the tagging process.

<b>💡 Usage Tips:</b>
• Use <code>/tagall</code> directly or reply to a message to tag from there  
• Use <code>/tagoff</code> to immediately stop if it's ongoing

<b>✨ Use this to gather users for VC, games, discussions or announcements!</b>
"""

HELP_42 = """
<b>🌐 Message Translator</b>

Easily translate any replied message into your desired language using Google-powered translation.

<b>🧩 Command:</b>

• ✧ <code>/tr</code> — <i>Reply to a text or caption</i>  
  ⤷ Automatically detects the source language and translates to English  
• ✧ <code>/tr hi</code> — <i>Reply to a message</i>  
  ⤷ Translate to Hindi (or any ISO code like <code>es</code> for Spanish)  
• ✧ <code>/tr en//fr</code> — <i>Reply to a message</i>  
  ⤷ Translate from English to French using custom source/destination

<b>🌍 Usage Tips:</b>
• Use ISO language codes (e.g., <code>en</code>, <code>hi</code>, <code>fr</code>, <code>ar</code>)  
• If no language is provided, it defaults to auto-detect ➤ English  
• Supports over 100 languages for input and output

<b>💡 Perfect for understanding multilingual messages instantly!</b>
"""

HELP_43 = """
<b>🗣️ Text-To-Speech (TTS)</b>

Convert any short message into a realistic Hindi voice note using Google TTS engine.

<b>🧩 Command:</b>
• ✧ <code>/tts your text here</code>  
  ⤷ Instantly generates a Hindi audio clip of your message

<b>🎙️ Example:</b>
• <code>/tts नमस्ते, आपका दिन शुभ हो!</code>

<b>🔤 Language Support:</b>
• Default language is Hindi (<code>hi</code>)  
• Multi-language support can be added on request

<b>💡 Great for sending voice wishes, quotes, or just fun messages!</b>
"""

HELP_44 = """
<b>📘 Urban Dictionary Lookup</b>

Fetches the modern or slang definition of any word from Urban Dictionary.

<b>🧩 Command:</b>
• ✧ <code>/ud &lt;word&gt;</code>  
  ⤷ Retrieves the most relevant definition and example usage

<b>🔍 Example:</b>
• <code>/ud savage</code>

<b>📄 Details:</b>
• Searches the Urban Dictionary for the given keyword  
• If no results are found, you'll be notified instantly  
• Also provides a Google link for extended context

<b>💡 Use this to understand trending slang, pop-culture words, or just for fun!</b>
"""

HELP_45 = """
<b>📤 Uploader Bot Features</b>

Easily upload media or text to online platforms and get shareable links.

<b>🧩 Commands:</b>
• ✧ <code>/tgm</code> — Reply to any media (photo, video, audio, document, animation, sticker, voice, video note) to upload it to <b>Catbox</b>  
• ✧ <code>/tgt</code> — Provide or reply to a text message to upload it to <b>Pastebin</b>

<b>🛠️ Usage:</b>

<b>1. Media Upload:</b>
• Reply to any supported media using the <code>/tgm</code> command  
• Supported media types: Photos, Videos, Audio, Documents, Animations, GIFs, Stickers, Voice messages, Video notes  
• The bot uploads the media to Catbox and returns a shareable link

<b>2. Text Upload:</b>
• Use <code>/tgt &lt;text&gt;</code> or reply to a message with <code>/tgt</code>  
• The bot uploads the text to Pastebin  
• A shareable link is returned for easy access

<b>🔗 Perfect for quick sharing and content storage!</b>
"""

HELP_46 = """
<b>🌐 Web Screenshot</b>

Take high-quality screenshots of websites directly from Telegram.

<b>🧩 Commands:</b>
• ✧ <code>/ss &lt;url&gt;</code> — Capture a screenshot of the given website
• ✧ <code>/webss &lt;url&gt;</code> — Alias for <code>/ss</code>
• ✧ <code>/screenshot &lt;url&gt;</code> — Alias for <code>/ss</code>

<b>📌 Examples:</b>
• <code>/ss google.com</code>
• <code>/ss https://github.com</code>

<b>⚙️ Notes:</b>
• You can skip <code>http://</code> or <code>https://</code>, it’ll be auto-corrected
• Screenshots are captured at <b>1280x800</b> resolution
• Requires <b>Playwright</b> installed on the server for full functionality
"""

HELP_47 = """
<b>💫 Make a Wish</b>

Make a wish and see how likely it is to come true — with a touch of magic!

<b>🧩 Command:</b>
• ✧ <code>/wish &lt;your wish&gt;</code> — Cast a wish and receive a randomized possibility percentage.
• ✧ <i>Reply to any message with</i> <code>/wish</code> — Sends a related wish animation with chance calculation.

<b>📌 Details:</b>
• If no wish is provided, the bot will prompt you to enter one.
• When a wish is sent, the bot replies with a random GIF and your wish's likelihood of success.

<b>🎉 Example:</b>
<code>/wish I want to win a lottery</code>
"""

HELP_48 = """
📝 <b>Write Command</b>

Turn your words into a handwritten note with this fun command!

<b>🧩 Command:</b>
• ✧ <code>/write</code> — Reply to a text message to generate a realistic paper-style handwritten image.

<b>📌 Usage:</b>
• Just type your message or reply to someone’s message with <code>/write</code> and watch it turn into a note!

<b>🎯 Example:</b>
• <code>/write Hello, how are you?</code>
"""
