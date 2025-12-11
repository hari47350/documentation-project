import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/search',
    component: ComponentCreator('/search', '822'),
    exact: true
  },
  {
    path: '/upload',
    component: ComponentCreator('/upload', 'e28'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'c13'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '593'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '5fe'),
            routes: [
              {
                path: '/docs/',
                component: ComponentCreator('/docs/', '0ee'),
                exact: true
              },
              {
                path: '/docs/modules/module1/Ingestion/week1',
                component: ComponentCreator('/docs/modules/module1/Ingestion/week1', '5df'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/Ingestion/week2',
                component: ComponentCreator('/docs/modules/module1/Ingestion/week2', '646'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/Ingestion/week3',
                component: ComponentCreator('/docs/modules/module1/Ingestion/week3', '7ae'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/Ingestion/week4',
                component: ComponentCreator('/docs/modules/module1/Ingestion/week4', 'ffe'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/OCR/week1',
                component: ComponentCreator('/docs/modules/module1/OCR/week1', 'b28'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/OCR/week2',
                component: ComponentCreator('/docs/modules/module1/OCR/week2', 'f07'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/OCR/week3',
                component: ComponentCreator('/docs/modules/module1/OCR/week3', 'b48'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/OCR/week4',
                component: ComponentCreator('/docs/modules/module1/OCR/week4', 'a29'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/Storage/week1',
                component: ComponentCreator('/docs/modules/module1/Storage/week1', '188'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/Storage/week2',
                component: ComponentCreator('/docs/modules/module1/Storage/week2', 'b97'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/Storage/week3',
                component: ComponentCreator('/docs/modules/module1/Storage/week3', '69b'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module1/Storage/week4',
                component: ComponentCreator('/docs/modules/module1/Storage/week4', '360'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamA/week5',
                component: ComponentCreator('/docs/modules/module2/teamA/week5', 'efd'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamA/week6',
                component: ComponentCreator('/docs/modules/module2/teamA/week6', '579'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamA/week7',
                component: ComponentCreator('/docs/modules/module2/teamA/week7', '8af'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamA/week8',
                component: ComponentCreator('/docs/modules/module2/teamA/week8', 'f81'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamB/week5',
                component: ComponentCreator('/docs/modules/module2/teamB/week5', '2d4'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamB/week6',
                component: ComponentCreator('/docs/modules/module2/teamB/week6', '87d'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamB/week7',
                component: ComponentCreator('/docs/modules/module2/teamB/week7', 'b5b'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamB/week8',
                component: ComponentCreator('/docs/modules/module2/teamB/week8', 'a6b'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamC/week5',
                component: ComponentCreator('/docs/modules/module2/teamC/week5', '463'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamC/week6',
                component: ComponentCreator('/docs/modules/module2/teamC/week6', 'a74'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamC/week7',
                component: ComponentCreator('/docs/modules/module2/teamC/week7', '763'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module2/teamC/week8',
                component: ComponentCreator('/docs/modules/module2/teamC/week8', '610'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamA/week10',
                component: ComponentCreator('/docs/modules/module3/teamA/week10', 'd15'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamA/week11',
                component: ComponentCreator('/docs/modules/module3/teamA/week11', 'a00'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamA/week12',
                component: ComponentCreator('/docs/modules/module3/teamA/week12', '92c'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamA/week9',
                component: ComponentCreator('/docs/modules/module3/teamA/week9', 'c3e'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamB/week10',
                component: ComponentCreator('/docs/modules/module3/teamB/week10', 'a61'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamB/week11',
                component: ComponentCreator('/docs/modules/module3/teamB/week11', '5d7'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamB/week12',
                component: ComponentCreator('/docs/modules/module3/teamB/week12', '3ec'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamB/week9',
                component: ComponentCreator('/docs/modules/module3/teamB/week9', 'e94'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamC/week10',
                component: ComponentCreator('/docs/modules/module3/teamC/week10', '641'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamC/week11',
                component: ComponentCreator('/docs/modules/module3/teamC/week11', '668'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamC/week12',
                component: ComponentCreator('/docs/modules/module3/teamC/week12', 'c2f'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module3/teamC/week9',
                component: ComponentCreator('/docs/modules/module3/teamC/week9', '3b8'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamA/week13',
                component: ComponentCreator('/docs/modules/module4/teamA/week13', 'f03'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamA/week14',
                component: ComponentCreator('/docs/modules/module4/teamA/week14', '31b'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamA/week15',
                component: ComponentCreator('/docs/modules/module4/teamA/week15', 'e06'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamA/week16',
                component: ComponentCreator('/docs/modules/module4/teamA/week16', '756'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamB/week13',
                component: ComponentCreator('/docs/modules/module4/teamB/week13', '55f'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamB/week14',
                component: ComponentCreator('/docs/modules/module4/teamB/week14', 'e7d'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamB/week15',
                component: ComponentCreator('/docs/modules/module4/teamB/week15', 'dc3'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamB/week16',
                component: ComponentCreator('/docs/modules/module4/teamB/week16', '4bf'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamC/week13',
                component: ComponentCreator('/docs/modules/module4/teamC/week13', '696'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamC/week14',
                component: ComponentCreator('/docs/modules/module4/teamC/week14', '604'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamC/week15',
                component: ComponentCreator('/docs/modules/module4/teamC/week15', '9cf'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/modules/module4/teamC/week16',
                component: ComponentCreator('/docs/modules/module4/teamC/week16', '99e'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/overview',
                component: ComponentCreator('/docs/overview', '3eb'),
                exact: true
              },
              {
                path: '/docs/test-snippet',
                component: ComponentCreator('/docs/test-snippet', 'f40'),
                exact: true
              },
              {
                path: '/docs/uploads/',
                component: ComponentCreator('/docs/uploads/', '2fe'),
                exact: true
              },
              {
                path: '/docs/uploads/upload-guide',
                component: ComponentCreator('/docs/uploads/upload-guide', '25d'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
