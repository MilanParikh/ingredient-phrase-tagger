def split_labels(label_reader,
                 training_label_writer,
                 testing_label_writer,
                 training_fraction,
                 max_labels=None):
    labels = _read_labels(label_reader, max_labels)
    _write_labels(labels, training_label_writer, testing_label_writer,
                  training_fraction)


def _read_labels(reader, max_labels):
    labels = []
    for i, label in enumerate(reader):
        if max_labels and i >= max_labels:
            break
        labels.append(label)
    return labels


def _write_labels(labels, training_label_writer, testing_label_writer,
                  training_fraction):
    training_label_count = int(len(labels) * training_fraction)
    training_label_writer.writerows(labels[:training_label_count])
    testing_label_writer.writerows(labels[training_label_count:])
