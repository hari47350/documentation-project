Project Overview

live website link 
https://documentation-project-4.onrender.com

This project demonstrates:

Building a documentation website using Docusaurus

Managing documentation with Markdown/MDX

Deploying a static site using Render

Handling real-world deployment issues (Node versioning, permissions, CI builds)

It is suitable for:

Technical documentation

Academic notes

Project documentation

Knowledge bases

🛠️ Tech Stack

Docusaurus 3 – Documentation framework

React 18 – Frontend UI library

Node.js 20 – Runtime environment

Markdown / MDX – Content authoring

Render – Static site hosting

GitHub – Version control & CI/CD

📂 Project Structure
documentation-project/
├── docs/               # Documentation content (Markdown/MDX)
├── src/                # React components
├── static/             # Static assets (images, icons, etc.)
├── docusaurus.config.js
├── sidebars.js
├── package.json
├── README.md
└── .nvmrc              # Node version configuration

▶️ How to Run Locally
Prerequisites

Node.js v20 or above

npm (comes with Node.js)

Steps
# 1. Clone the repository
git clone https://github.com/hari47350/documentation-project.git

# 2. Navigate into the project folder
cd documentation-project

# 3. Install dependencies
npm install

# 4. Start the development server
npm start

Open in browser
http://localhost:3000


The site will automatically reload when you make changes.

🏗️ Build for Production

To generate production-ready static files:

npm run build


The output will be created in the build/ directory.

🚀 Deployment

The project is deployed as a Static Site on Render

Deployment is triggered automatically on every push to the main branch

Node version is enforced using .nvmrc

🔒 Environment Variables

This project does not require any environment variables for deployment.

📌 Key Learnings

Static site deployment with CI/CD

Node.js version management in cloud platforms

Handling permission and runtime issues in builds

Professional project documentation practices

📄 License

This project is for educational and learning purposes.

👤 Author

Hari Krishna Reddy
GitHub: https://github.com/hari47350
