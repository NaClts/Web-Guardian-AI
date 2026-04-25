import fcntl
import os
import sys

if __name__ == "__main__":
    path = sys.argv[1]
    text = sys.argv[2]

    with open(path, "a") as f:        # append mode
        fcntl.flock(f, fcntl.LOCK_EX) # block until lock acquired
        try:
            f.write(text + "\n")
            f.flush()
            os.fsync(f.fileno())      # optional: force write to disk
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
