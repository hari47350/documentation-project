// docusaurus.config.js

/** @type {import('@docusaurus/types').Config} */

let lightCodeTheme;
let darkCodeTheme;

try {
  lightCodeTheme = require('prism-react-renderer/themes/github');
  darkCodeTheme = require('prism-react-renderer/themes/dracula');
} catch (err) {
  console.warn(
    'prism-react-renderer theme import failed — falling back to defaults:',
    err.message
  );
  lightCodeTheme = undefined;
  darkCodeTheme = undefined;
}

const config = {
  // ===== BASIC SITE INFO =====
  title: 'SmartIDH Docs',
  tagline: 'Internal documentation for SmartIDH3 project',
  url: 'http://localhost',
  baseUrl: '/',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  organizationName: 'zasya',      // can be anything, internal only
  projectName: 'smartidh-docs',

  // ===== PRESETS =====
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: 'docs',
          routeBasePath: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: undefined,
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  // ===== THEME CONFIG =====
  themeConfig: {
    // 🌙 Make dark mode default
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,          // user can still switch if they want
      respectPrefersColorScheme: false,
    },

    navbar: {
      title: 'SmartIDH Docs',
      logo: {
        alt: 'Zasya SmartIDH logo',
        src: 'img/zasya-logo.png',   // <-- your image in static/img/zasya-logo.png
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          label: 'Docs',
          position: 'left',
        },
        {
          to: '/upload',
          label: 'Upload',
          position: 'left',
        },
      ],
    },

    footer: {
      style: 'dark',
      copyright: `© ${new Date().getFullYear()} Zasya SmartIDH`,
    },

    prism: {
      theme: lightCodeTheme,
      darkTheme: darkCodeTheme,
      additionalLanguages: [
        'bash',
        'powershell',
        'json',
        'java',
        'python',
        'mongodb',
      ],
    },
  },

  themes: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en'],
      },
    ],
  ],
};

module.exports = config;