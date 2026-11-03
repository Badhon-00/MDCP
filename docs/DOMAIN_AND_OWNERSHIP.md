# Custom domain, copyright and brand ownership

This guide prepares the MDCP website for a domain that you register and control. It cannot purchase a domain or file a trademark on your behalf.

## 1. Register the domain in your own name

1. Choose a domain registrar and register using your own legal name, email address and payment method. Keep access to the registrar account and registrant email.
2. Enable two-factor authentication, registrar lock and auto-renew. Save recovery codes offline.
3. Use a brand/domain that does not imply endorsement by Anthropic, OpenAI, GitHub or another third party. Avoid placing their product names in your domain.
4. Keep invoices and registration confirmation as proof of account ownership.

A domain is controlled through the registrar account and registrant records; a DNS configuration alone does not establish legal ownership.

## 2. Verify the domain before connecting it

GitHub recommends verifying a custom domain at account level before assigning it to a Pages site. In GitHub Profile → Settings → Pages → Add a domain, enter your domain and publish the TXT record GitHub provides. Keep that TXT record in DNS after verification. This reduces the risk of another GitHub user claiming a domain after a repository or Pages configuration changes.

Official guide: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages

## 3. Connect it to MDCP GitHub Pages

In Badhon-00/MDCP → Settings → Pages → Custom domain, enter the exact domain and save. Because MDCP publishes through a custom GitHub Actions workflow, GitHub says a committed CNAME file is not required for that publishing mode.

For an apex domain such as example.com, GitHub currently documents these A records:

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

For www.example.com, create a CNAME record with name www and value badhon-00.github.io. GitHub recommends configuring both apex and www variants where appropriate. Check the official documentation again before applying records, because provider instructions can change.

Official guide: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

After DNS propagates, confirm the domain in GitHub Pages and enable Enforce HTTPS when the certificate is ready. DNS propagation and certificate issuance can take time. Avoid wildcard DNS records.

## 4. Copyright and third-party material

Copyright in original creative work generally arises automatically; registration and evidence requirements depend on jurisdiction. Keep source history, design files, contributor agreements, invoices and dated records.

You can claim rights only in original material you or authorized contributors created. MDCP includes third-party skills and dependencies; their original authors retain their own rights and their licenses/attribution requirements continue to apply. The repository's MIT license permits broad reuse of covered original code; it does not make every bundled skill exclusively yours.

Do not remove third-party license notices or claim ownership of upstream work. For contributions, preserve author credit and clarify licensing before relicensing.

## 5. Trademark in Bangladesh

A repository notice or use of a name is not the same as a registered trademark. Before filing:
1. Search for identical and confusingly similar marks in relevant goods/services classes.
2. Decide the actual mark (word mark, logo, or both) and the legal owner.
3. Check the applicable filing requirements and fees with Bangladesh's Department of Patents, Designs and Trademarks (DPDT).
4. Consider a local IP lawyer for clearance and filing.

Official authority: https://dpdt.gov.bd/

No registration or exclusive right is claimed by this guide. A trademark filing is a separate legal process, and approval is not guaranteed.

## 6. Suggested order

1. Choose and clear a distinct project brand.
2. Register the domain in your own name and secure the registrar account.
3. Verify the domain in GitHub account settings.
4. Add it to the repository's Pages settings and configure DNS.
5. Wait for HTTPS, then test apex/www, mobile, desktop and all asset links.
6. Consult DPDT or an IP lawyer before filing the trademark.
