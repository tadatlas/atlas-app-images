# Atlas App Images

Images used in the **Atlas iQ** app (Softr). This repo is public so the images can be served through the free jsDelivr CDN.

## What's here

| File | What it shows |
| --- | --- |
| `Market Intelligence.png` | Dark concrete interior with a terracotta chair, lit by late sun |
| `image3.png` | Two-storey modern home at dusk, windows lit warm |

## How to link to an image

Use the jsDelivr link, not the GitHub page link:

```
https://cdn.jsdelivr.net/gh/tadatlas/atlas-app-images@main/<file name>
```

Spaces in a file name become `%20`. For example:

```
https://cdn.jsdelivr.net/gh/tadatlas/atlas-app-images@main/Market%20Intelligence.png
https://cdn.jsdelivr.net/gh/tadatlas/atlas-app-images@main/image3.png
```

## House rules

1. **Never rename, move or delete a file that's already in use.** The app links to the exact file name, so the image disappears the moment it changes.
2. **Name new files clearly before uploading.** Lower case, hyphens, no spaces: `market-intelligence-hero.png`, not `image3.png`.
3. **To swap an image, upload it under a new name** and point the app at the new link. Replacing a file with the same name can take up to 12 hours to show, because jsDelivr caches it.
4. **Keep each file under 20 MB.** jsDelivr won't serve anything larger.
5. **Update the table above** whenever you add an image, so you know what each file is for.

## Adding an image (on github.com)

1. Open this repo and click **Add file → Upload files**.
2. Drag the image in.
3. Under **Commit changes**, write a short note (e.g. `Add Explore tile image for Offices`) and keep **Commit directly to the main branch** selected.
4. Click **Commit changes**. The jsDelivr link works within a minute or two.
