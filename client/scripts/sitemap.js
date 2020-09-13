
require('babel-register')({
    presets: [
        'env',
    ],
});

const config = require('../src/config')

const fs = require('fs');



function createSitemap() {

    const sitemap = fs.createWriteStream(`../public/sitemap.xml`);

    let text = `<?xml version="1.0" encoding="UTF-8"?>\n`

    text += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`

    sitemap.write(text);

    const baseUrl = `<url>\n<loc>https://gisjobsmap.com/</loc>\n<changefreq>daily</changefreq>\n<priority>0.8</priority>\n</url>`

    sitemap.write(baseUrl);

    config.availableCountries.forEach((row) => {
        sitemap.write(`<url>\n`);
        sitemap.write(`<loc>https://gisjobsmap.com/${row.iso2}</loc>\n`);
        sitemap.write(`<changefreq>daily</changefreq>\n`);
        sitemap.write(`</url>\n`);
    });

    sitemap.write(`</urlset>\n`);

    console.log('done')
}

createSitemap()






// getData(count);