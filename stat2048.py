import ai2048

from sys import argv

OUT_FOLDER = "output"

def main():
    # Take in cmd line args: number of trials and output location

    if len(argv) < 3:
        print("Usage: `python3 {} <ai> <ntrials> [output_file] [other args]`".format(argv[0]))
        print("    ai: AI Agent to run test")
        print("        rand: Random AI (default)")
        print("        greed: Greedy AI")
        print("        adls: Greedy AI")
        print("    ntrials: Number of trials to run")
        print("    output_file: Name of the Output File for Results")
        print("    other args: Other arguments")
        print("        Avg DLS: [depth] [iterations]")
        return

    ai_type = argv[1]
    match ai_type:
        case 'rand':
            ai_type = "Random AI"
            instance = ai2048.RandomAI()
        case 'greed':
            ai_type = "Greedy AI"
            instance = ai2048.GreedyAI()
        case 'mc':
            if len(argv) < 6:
                depth = 3
                iterations = 8
            else:
                depth = int(argv[4])
                iterations = int(argv[5])

            ai_type = "Simple Monte-Carlo"
            instance = ai2048.SimpleMonteCarloAI(depth, iterations)
        case 'adls':
            if len(argv) < 6:
                depth = 3
                iterations = 8
            else:
                depth = int(argv[4])
                iterations = int(argv[5])

            ai_type = "ADLS AI"
            instance = ai2048.AveragedDLS(depth, iterations)
        case _:
            print("Unknown Options Chosen, Using RandomAI...")
            instance = ai2048.RandomAI()

    n_trials = int(argv[2])
    output_filename = "output.txt"

    if len(argv) >= 4:
        output_filename = OUT_FOLDER + "/" + argv[3] + ".txt"

    with open(output_filename, "w") as fd:
        fd.write("=== Results using {} ===\n".format(ai_type))

        sum_score = 0
        tile_freq = {}

        for trial_n in range(n_trials):
            print("Iteration {} of {}".format(trial_n+1, n_trials))

            instance.start()

            while not instance.terminal():
                instance.make_move()

            score = instance.score
            max_tile = instance.get_max_tile()

            sum_score += score
            if max_tile in tile_freq:
                tile_freq[max_tile] += 1
            else:
                tile_freq[max_tile] = 1

            fd.write("[{:>3}] Score: {:>6}, Max Tile Value: {:>4}\n".format(trial_n+1, instance.score, instance.get_max_tile()))

        fd.write("Average Score: {}\n".format(sum_score/n_trials))
        fd.write("Tile Frequency:\n")
        for tile_val in sorted(tile_freq.keys()):
            fd.write("    {:>4}: {:6.2f}%\n".format(tile_val, tile_freq[tile_val]*100/n_trials))

    return

if __name__ == "__main__":
    main()
