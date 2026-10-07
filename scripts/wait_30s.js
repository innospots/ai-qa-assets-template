var start = Date.now();
while (Date.now() - start < 30000) {
  // busy wait 30 seconds for assistant reply
}
output.waitDone = true;
