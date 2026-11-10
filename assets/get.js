/* Ticerapps download links (/get/<app>/).
   Sends each visitor to the right store for their device. It reads only the browser's
   user agent and this page's query string, stores nothing, and loads nothing else.

   Store targets come from data attributes on <body>:
     data-ios       App Store URL for iPhone and iPad (empty: not on the App Store yet)
     data-android   Google Play URL (empty: not on Google Play yet)
     data-mac       URL for Macs (optional, e.g. a Mac App Store listing)
     data-desktop   URL for other computers (optional)
     data-fallback  where anyone else goes (the app's page)
     data-apple-pt  App Store Connect provider token, for App Store campaign links (optional)

   Campaign tags in the link are passed on to the stores. Either form works:
     ?src=tiktok&c=launch-week
     ?utm_source=tiktok&utm_medium=paid_social&utm_campaign=launch-week&utm_content=video-a
   Google Play receives them as its install referrer (Play Console > acquisition reports).
   The App Store receives ct=<source>-<campaign> when data-apple-pt is set.
   Add ?stay to the link to see this page without being redirected. */
(function () {
  var d = document.body.dataset;
  var q = new URLSearchParams(location.search);
  var ua = navigator.userAgent || '';

  var isBot = /bot|crawl|spider|slurp|facebookexternalhit|embedly|preview|lighthouse|headless/i.test(ua);
  var isIOS = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  var isAndroid = !isIOS && /Android/i.test(ua);
  var isMac = !isIOS && /Macintosh/.test(ua);

  function tag(name, short) { return (q.get('utm_' + name) || (short && q.get(short)) || '').trim(); }
  var source = tag('source', 'src'), medium = tag('medium'), campaign = tag('campaign', 'c'), content = tag('content');
  var tagged = source || medium || campaign || content;

  function forPlay(url) {
    if (!url || !tagged) return url;
    var parts = ['utm_source=' + encodeURIComponent(source || 'ticerapps.com')];
    if (medium) parts.push('utm_medium=' + encodeURIComponent(medium));
    if (campaign) parts.push('utm_campaign=' + encodeURIComponent(campaign));
    if (content) parts.push('utm_content=' + encodeURIComponent(content));
    return url + (url.indexOf('?') < 0 ? '?' : '&') + 'referrer=' + encodeURIComponent(parts.join('&'));
  }
  function forApple(url) {
    if (!url || !tagged || !d.applePt) return url;
    var ct = [source, campaign || content].filter(Boolean).join('-').slice(0, 40);
    return url + (url.indexOf('?') < 0 ? '?' : '&') + 'pt=' + encodeURIComponent(d.applePt) +
      '&ct=' + encodeURIComponent(ct) + '&mt=8';
  }

  var ios = forApple(d.ios), android = forPlay(d.android);
  // The store buttons carry the same campaign tags as the redirect.
  var appleBtn = document.querySelector('[data-store="ios"]');
  var playBtn = document.querySelector('[data-store="android"]');
  if (appleBtn && ios) appleBtn.href = ios;
  if (playBtn && android) playBtn.href = android;

  var target = isIOS ? (ios || d.fallback)
    : isAndroid ? (android || d.fallback)
    : isMac ? (d.mac ? forApple(d.mac) : d.desktop || d.fallback)
    : (d.desktop || d.fallback);

  var status = document.getElementById('status');
  var label = isIOS && ios ? 'Opening the App Store…'
    : isAndroid && android ? 'Opening Google Play…'
    : (isIOS || isAndroid) ? 'Not in your store yet. Taking you to the app page…'
    : '';

  if (q.has('stay') || isBot || !target) {
    if (status && q.has('stay')) status.textContent = 'Preview: this device would go to ' + target;
    return;
  }
  if (status && label) status.textContent = label;
  location.replace(target);
})();
