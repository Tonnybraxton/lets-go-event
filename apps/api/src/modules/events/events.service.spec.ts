import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { distanceBetweenKm } from "./geo.js";

describe("distanceBetweenKm", () => {
  it("returns zero for the same coordinates", () => {
    assert.equal(
      distanceBetweenKm(
        { latitude: -1.2676, longitude: 36.8108 },
        { latitude: -1.2676, longitude: 36.8108 },
      ),
      0,
    );
  });

  it("calculates a plausible Westlands-to-Kilimani distance", () => {
    const distance = distanceBetweenKm(
      { latitude: -1.2676, longitude: 36.8108 },
      { latitude: -1.2929, longitude: 36.7854 },
    );
    assert.ok(distance > 3);
    assert.ok(distance < 6);
  });
});
