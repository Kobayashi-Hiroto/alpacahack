import express from "express";
import rateLimit from "express-rate-limit";

const FLAG = process.env.FLAG ?? console.log("No flag") ?? process.exit(1);

const app = express();
app.use(express.json());
app.use(express.static("public"));
app.use("/api", rateLimit({ windowMs: 60 * 1000, max: 4, }));

app.post("/api/crawl-request", async (req, res) => {
  const url = req.body?.url;
  if (typeof url !== "string" || (!url.startsWith("http://") && !url.startsWith("https://")))
    return res.status(400).send("Invalid url");
  try {
    const r = await fetch(url, { headers: { FLAG }, signal: AbortSignal.timeout(5000) }); // !!
    if (!r.ok) return res.status(502).send("Fetch failed");
    return res.sendStatus(200);
  } catch (e) {
    return res.status(500).send(`Something wrong: ${e.name}`);
  }
});

app.listen(3333);
