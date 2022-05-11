import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input file')
parser.add_argument('output', type=str, help='Output file')
parser.add_argument('-s', '--stats', action='store_true', help='Print stats graphs')

X, Y, Z = [], [], []

args = parser.parse_args()

with open(args.input, 'r') as f:
    ply = f.readlines()
    end_header = ply.index('end_header\n')
    olines = []
    # group every two lines together into one line after the end_header index
    for i in range(end_header + 1, len(ply), 2):
        xyz = ply[i].split(' ')
        rgb = ply[i+1].split(' ')
        x = float(xyz[0]) # - left -> + right
        y = float(xyz[1]) # - top -> + bottom
        z = -float(xyz[2]) # - front -> + back (it's never actually negative)
        r = float(rgb[0])
        g = float(rgb[1])
        b = float(rgb[2])

        X.append(x)
        Y.append(y)
        Z.append(z)

        olines.append(f'{x:.6f} {z:.6f} {y:.6f} {r:.6f} {g:.6f} {b:.6f}\n')
    # write the output file
    with open(args.output, 'w') as f:
        f.writelines(olines)

print(f'Converted a point cloud with {len(X)} points to txt format (similar to S3DIS). Saved to {args.output}.')

if args.stats:
    import numpy as np
    import matplotlib.pyplot as plt
    plt.subplots(1, 3, figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.hist(X, bins=30)
    plt.title(f'mean={np.mean(X):.6f}, std={np.std(X):.6f}')
    plt.xlabel('X')
    plt.subplot(1, 3, 2)
    plt.hist(Y, bins=30)
    plt.title(f'mean={np.mean(Y):.6f}, std={np.std(Y):.6f}')
    plt.xlabel('Y')
    plt.subplot(1, 3, 3)
    plt.hist(Z, bins=30)
    plt.title(f'mean={np.mean(Z):.6f}, std={np.std(Z):.6f}')
    plt.xlabel('Z')
    plt.show()