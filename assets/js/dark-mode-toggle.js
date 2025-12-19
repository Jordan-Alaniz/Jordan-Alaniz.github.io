document.addEventListener('DOMContentLoaded', () => {
  // Check system preference at first load
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  // Create toggle button
  const toggle = document.createElement('button');
  toggle.textContent = '🌓';
  toggle.style.position = 'fixed';
  toggle.style.bottom = '1rem';
  toggle.style.right = '1rem';
  toggle.style.zIndex = '9999';
  toggle.style.padding = '0.5rem';
  toggle.style.borderRadius = '0.3rem';
  toggle.style.background = '#444';
  toggle.style.color = '#fff';
  toggle.style.border = 'none';
  toggle.style.cursor = 'pointer';

  toggle.onclick = () => {
    if (document.documentElement.getAttribute('data-theme') === 'dark') {
      document.documentElement.setAttribute('data-theme', 'light');
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  };

  document.body.appendChild(toggle);
});
