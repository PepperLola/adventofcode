use std::hint::black_box;

use criterion::{criterion_group, criterion_main, Criterion};

extern crate aoc_utils;

use aoc_utils::{find_all_grid};

fn generate_grid(h: usize, w: usize) -> Vec<i64> {
    (0..h*w).map(|i| (i % 10) as i64).collect()
}

fn generate_pattern(h: usize, w: usize) -> Vec<i64> {
    (0..h*w).map(|i| (i % 3) as i64).collect()
}

fn bench_find_all(c: &mut Criterion) {
    let grid_h = 1000;
    let grid_w = 500;
    let pat_h = 5;
    let pat_w = 5;

    let grid = generate_grid(grid_h, grid_w);
    let pat = generate_pattern(pat_h, pat_w);

    let max_out = 10_000;
    let mut out_buf = vec![0usize; max_out*2];

    c.bench_function("find_all_grid", |b| {
        b.iter(|| {
            let count = find_all_grid(
                grid.as_ptr(),
                grid_h,
                grid_w,
                pat.as_ptr(),
                pat_h,
                pat_w,
                out_buf.as_mut_ptr(),
                max_out,
            );
            black_box(count);
        });
    });
}

criterion_group!(benches, bench_find_all);
criterion_main!(benches);
