/*
 * Live character counts under the SEO title and meta description inputs.
 * The count turns to a warning past the recommended length, which search
 * engines truncate; the database still accepts a little more.
 */
(function () {
  const LIMITS = [
    [/(^|_)seo_title(_ar)?$/, 60],
    [/(^|_)meta_description(_ar)?$/, 160],
  ];

  function attach(input, limit) {
    const note = document.createElement('div');
    note.className = 'ap-seo-count';
    note.setAttribute('aria-live', 'polite');
    input.insertAdjacentElement('afterend', note);
    const update = () => {
      const length = input.value.length;
      note.textContent = `${length} / ${limit} characters`;
      note.classList.toggle('ap-overdue', length > limit);
    };
    input.addEventListener('input', update);
    update();
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[name], textarea[name]').forEach((input) => {
      const match = LIMITS.find(([pattern]) => pattern.test(input.name));
      if (match) attach(input, match[1]);
    });
  });
})();
