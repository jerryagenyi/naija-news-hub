const { spawn } = require('child_process');
const readline = require('readline');

// Start the Context7 MCP server
const context7Process = spawn('npx', ['-y', '@upstash/context7-mcp@latest']);

// Set up readline interface to read from the process
const rl = readline.createInterface({
  input: context7Process.stdout,
  terminal: false
});

// Listen for data from the server
rl.on('line', (line) => {
  if (line.includes('running on stdio')) {
    console.log('Context7 server is running. Sending query...');
    
    // Send a query about React hooks
    const query = JSON.stringify({
      name: "search",
      arguments: {
        query: "React hooks documentation"
      }
    });
    
    context7Process.stdin.write(query + '\n');
  } else if (line.startsWith('{')) {
    try {
      // Try to parse the response as JSON
      const response = JSON.parse(line);
      console.log('Received response from Context7:');
      console.log(JSON.stringify(response, null, 2));
      
      // Close the process after getting a response
      context7Process.kill();
      process.exit(0);
    } catch (e) {
      console.log('Received non-JSON response:', line);
    }
  } else {
    console.log('Server output:', line);
  }
});

// Handle errors
context7Process.stderr.on('data', (data) => {
  console.error(`Error: ${data}`);
});

// Handle process exit
context7Process.on('close', (code) => {
  console.log(`Context7 process exited with code ${code}`);
});

// Set a timeout to kill the process if it doesn't respond
setTimeout(() => {
  console.log('Timeout reached. Killing Context7 process...');
  context7Process.kill();
  process.exit(1);
}, 30000);
