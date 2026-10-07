var start = Date.now();
while (Date.now() - start < 60000) {
  // busy wait 60 seconds
}
output.waitDone = true;
