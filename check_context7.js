// Simple script to check if Context7 MCP server is running
const { exec } = require('child_process');

// Check for running Node.js processes that might be the Context7 server
exec('ps aux | grep "context7\\|upstash" | grep -v grep', (error, stdout, stderr) => {
  if (error) {
    console.log('No Context7 server processes found running.');
    return;
  }
  
  if (stdout) {
    console.log('Potential Context7 server processes found:');
    console.log(stdout);
  } else {
    console.log('No Context7 server processes found running.');
  }
});

// Try to connect to the Context7 server directly (this is a simplified example)
console.log('Note: This script cannot directly check VS Code\'s internal connection to Context7.');
console.log('If you see Context7 processes running above, it\'s a good sign that the server is available.');
console.log('To fully verify, try using Context7 functionality within VS Code.');
