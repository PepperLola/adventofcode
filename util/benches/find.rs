use std::hint::black_box;

use criterion::{criterion_group, criterion_main, Criterion};

extern crate aoc_utils;

use aoc_utils::{find_grid};

fn generate_grid(h: usize, w: usize) -> Vec<i64> {
    (0..h*w).map(|i| (i % 10) as i64).collect()
}

fn generate_pattern(h: usize, w: usize) -> Vec<i64> {
    (0..h*w).map(|i| (i % 3) as i64).collect()
}

fn bench_find(c: &mut Criterion) {
    let grid_h = 1000;
    let grid_w = 500;
    let pat_h = 5;
    let pat_w = 5;

    let grid = generate_grid(grid_h, grid_w);
    let pat = generate_pattern(pat_h, pat_w);

    let mut out_x: usize = 0;
    let mut out_y: usize = 0;

    c.bench_function("find_grid", |b| {
        b.iter(|| {
            let count = find_grid(
                grid.as_ptr(),
                grid_h,
                grid_w,
                pat.as_ptr(),
                pat_h,
                pat_w,
                &mut out_x,
                &mut out_y,
            );
            black_box(count);
        });
    });
}

criterion_group!(benches, bench_find);
criterion_main!(benches);
