const std = @import("std");

var prng: std.Random.DefaultPrng = undefined;

export fn init() void {
    prng = std.Random.DefaultPrng.init(blk: {
        var seed: u64 = undefined;
        std.posix.getrandom(std.mem.asBytes(&seed)) catch {
            seed = @intCast(std.time.timestamp());
        };
        break :blk seed;
    });
}

export fn roll(x: u8, y: u8) u16 {
    const rand = prng.random();
    var result: u16 = 0;
    for (0..x) |_| {
        result += rand.intRangeAtMost(u8, 1, y);
    }
    return result;
}
