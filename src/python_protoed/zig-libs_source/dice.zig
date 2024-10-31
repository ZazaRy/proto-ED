const std = @import("std");

export fn roll(x: u8, y: u8) u8 {
    var prng = std.Random.DefaultPrng.init(blk: {
        var seed: u64 = undefined;
        std.posix.getrandom(std.mem.asBytes(&seed)) catch {
            seed = @intCast(std.time.timestamp());
        };
        break :blk seed;
    });
    const rand = prng.random();
    var result: u8 = 0 ;
    for (0..x) |i| {
        _ = i;
        result += rand.intRangeAtMost(u8,1,y);
    }
    return result;
}
