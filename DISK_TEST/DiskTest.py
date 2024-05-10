import tqdm
import os
import time


def write_to_disk(output_file, block_size, total_size, unit, target_disk):
    unit_to_bytes = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
    bytes_per_unit = unit_to_bytes.get(unit.upper(), 1)

    with open(os.path.join(target_disk, output_file), "wb") as f:
        with tqdm.tqdm(
            total=max(total_size / bytes_per_unit, 1),
            unit=unit,
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            bytes_written = 0
            start_time = time.time()
            while bytes_written < total_size:
                # Write data to disk
                chunk_size = min(block_size, total_size - bytes_written)
                f.write(
                    b"\x00" * chunk_size
                )  # Writing zeros for demonstration, replace with actual data
                bytes_written += chunk_size

                # Update progress bar
                pbar.update(chunk_size / bytes_per_unit)

                # Calculate and display speed
                elapsed_time = time.time() - start_time
                try:
                    speed = bytes_written / elapsed_time
                except ZeroDivisionError:
                    speed = 0
                pbar.set_postfix(
                    speed="{:.2f} {}/s".format(speed / bytes_per_unit, unit)
                )


if __name__ == "__main__":
    try:
        output_file = "test_file.bin"  # Change the output file name as needed
        block_size = 1 * 1024  # Change the block size as needed (in bytes)
        total_size = (
            10000 * 1024 * 1024
        )  # Total size of the file to write (100 MB in this case)
        selected_unit = "MB"  # Default unit (can be 'B', 'KB', 'MB', 'GB')
        target_disk = "Q:/"  # Change the target disk as needed

        write_to_disk(output_file, block_size, total_size, selected_unit, target_disk)
        filepath = os.path.join(target_disk, output_file)
        if os.path.exists(filepath):
            os.remove(filepath)
        print("Test complete.")
    except Exception as e:
        print("KeyboardInterrupt, removing temp file.", str(e))
        filepath = os.path.join(target_disk, output_file)
        if os.path.exists(filepath):
            os.remove(filepath)
