# Your own domain, and what you can and cannot own

This is practical information, not legal advice. For a trademark or a license change, ask a lawyer in your country.

## 1. Get a domain you fully own

1. Pick a registrar and register **in your own name and your own email**: for example Cloudflare Registrar, Namecheap, Porkbun or Google-backed registrars. The account holder is the owner, so never let a friend, a freelancer or a tool register it for you.
2. Turn on two-factor authentication on the registrar account. Turn on auto-renew, registrar lock and WHOIS privacy. Register for several years if you can.
3. Keep the registrant email on an inbox you will always control.
4. Avoid "claude", "anthropic", "openai", "gpt" or "codex" in the domain or the brand. Those are other companies' trademarks; a name containing them can be taken from you and can confuse users into thinking the project is official.

## 2. Point it at GitHub Pages (the Skill Explorer in `site/`)

In the repository: Settings, Pages, **Custom domain**, enter the domain, Save. The site is deployed by GitHub Actions, so you do not add a `CNAME` file; the setting is enough.

At your DNS provider:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `<your-github-username>.github.io` |

Then tick **Enforce HTTPS** once GitHub finishes the certificate (it can take up to a day). Also verify the domain at account level (Settings, Pages, Add a domain, add the TXT record GitHub shows). That stops anyone else from claiming your domain on their own Pages site. Check GitHub's Pages documentation for the current IP addresses before you copy them.

## 3. Copyright

- Copyright in what you write yourself exists automatically, with no registration, in countries that follow the Berne Convention (Bangladesh is a member). Registration is optional and mostly helps when you must prove it.
- **You own only your own files.** In this repository those are `master-developer`, `mdcp-self-check`, `mdcp-token-meter`, `omniroute-free-llm-routing`, the scripts, the agent fabric, the site and the docs you or your tools wrote. See "Original to this repository" in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
- **You do not own the bundled skills** (ECC, Anthropic, Vercel, Superpowers, Three.js, replica, UI/UX Pro Max and others). Their authors keep copyright, and their licenses (MIT, Apache-2.0) require you to keep their notices. You cannot claim "all rights reserved" on them, and you should not remove the credits.
- The MIT license on your own files lets anyone use, copy and fork them. That is what makes forks, stars and adoption possible. If you want full control instead, use a restrictive license, but expect far less use. Contributors keep copyright in what they contribute; to relicense later you would need their agreement (a contributor license agreement).

## 4. Trademark

- A trademark is not automatic. Using a name gives you weak, local rights at best. Strong rights come from **registering** with your national trademark office (in Bangladesh, the Department of Patents, Designs and Trademarks) and, later, abroad.
- Before you invest, search that the name is free. "MDCP" is a short acronym that other organizations may already use, in the trademark register and on the web.
- The long name "Master Developer **Claude** Plugin" contains Anthropic's trademark. You cannot register a mark that includes it, and it can suggest the project is official. Consider keeping "MDCP" as the brand and describing it as "a plugin for Claude Code" (descriptive use), not as part of the name.
- Once you choose a name, use it consistently, add a trademark notice in the README, and register the domain, the GitHub organization and the social handles under it at the same time.

## 5. A good order of work

1. Choose and clear the name (trademark search, domain available, no other company's marks inside it).
2. Register the domain and secure the accounts.
3. Connect the domain to Pages.
4. File the trademark application.
5. Update README, LICENSE copyright line and site footer to the final name.
