class QualifiedNameHelper():

    _default_delimiter = "."

    @staticmethod
    def concat_save_with_delimiter(delimiter, *names):
        return delimiter.join([n for n in names if n]) # is non-empty string
    
    @staticmethod
    def concat_save(*names):
        return QualifiedNameHelper.concat_save_with_delimiter(QualifiedNameHelper._default_delimiter, *names)