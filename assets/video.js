/* Ticerapps click-to-play videos.
   Each .video[data-yt] shows a still image hosted on this site, linked to the video on YouTube.
   Nothing is loaded from YouTube until the visitor presses play; then the still is swapped for
   YouTube's no-cookie player. Without JavaScript the link simply opens the video on YouTube.
   The player needs a referrer to load, so the iframe sends this page's origin even though the
   pages themselves send none. This script stores nothing. */
(function () {
  document.querySelectorAll('.video[data-yt]').forEach(function (box) {
    var link = box.querySelector('a');
    if (!link) return;
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var id = box.getAttribute('data-yt');
      if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
      var frame = document.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1';
      frame.title = box.getAttribute('data-title') || 'Video';
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      box.replaceChild(frame, link);
      frame.focus();
    });
  });
})();
