

from PySide import QtGui
from mapclientplugins.createhemispheremodelstep.ui_configuredialog import Ui_ConfigureDialog

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''

STRING_FLOAT_FORMAT = '{:.5g}'

class ConfigureDialog(QtGui.QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)

        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._makeConnections()

    def _makeConnections(self):
        self._ui.lineEdit0.textChanged.connect(self.validate)
        self._ui.elementsAroundLineEdit.textChanged.connect(self._elementsAroundLineEditEntered)
        self._ui.elementsUpLineEdit.textChanged.connect(self._elementsUpLineEditEntered)
        self._ui.elementsAlongStemLineEdit.textChanged.connect(self._elementsAlongStemLineEditEntered)
        #self._ui.radiusLineEdit.textChanged.connect(self._radiusLineEditEntered)
        #self._ui.stemLengthLineEdit.textChanged.connect(self._stemLengthLineEditEntered)

    def accept(self):
        '''
        Override the accept method so that we can confirm saving an
        invalid configuration.
        '''
        result = QtGui.QMessageBox.Yes
        if not self.validate():
            result = QtGui.QMessageBox.warning(self, 'Invalid Configuration',
                'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if result == QtGui.QMessageBox.Yes:
            QtGui.QDialog.accept(self)

    def validate(self):
        '''
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        '''
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        value = self.identifierOccursCount(self._ui.lineEdit0.text())
        valid = (value == 0) or (value == 1 and self._previousIdentifier == self._ui.lineEdit0.text())
        if valid:
            self._ui.lineEdit0.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEdit0.setStyleSheet(INVALID_STYLE_SHEET)

        return valid

    def getConfig(self):
        '''
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        '''
        self._previousIdentifier = self._ui.lineEdit0.text()
        config = {}
        config['identifier'] = self._ui.lineEdit0.text()
        config['elements around'] = self._parseInt(self._ui.elementsAroundLineEdit, 12)
        config['elements up'] = self._parseInt(self._ui.elementsUpLineEdit, 3)
        config['elements along stem'] = self._parseInt(self._ui.elementsAlongStemLineEdit, 1)
        #config['radius'] = self._parseReal(self._ui.radiusLineEdit, 1.0)
        #config['stem length'] = self._parseReal(self._ui.stemLengthLineEdit, 0.5)
        return config

    def setConfig(self, config):
        '''
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        '''
        self._previousIdentifier = config['identifier']
        self._ui.lineEdit0.setText(config['identifier'])
        self._displayInt(self._ui.elementsAroundLineEdit, config['elements around'])
        self._displayInt(self._ui.elementsUpLineEdit, config['elements up'])
        self._displayInt(self._ui.elementsAlongStemLineEdit, config['elements along stem'])
        #self._displayReal(self._ui.radiusLineEdit, config['radius'])
        #self._displayReal(self._ui.stemLengthLineEdit, config['stem length'])

    def _displayInt(self, widget, value):
        newText = str(value)
        widget.setText(newText)

    def _parseInt(self, widget, oldValue):
        valueText = widget.text()
        try:
            value = int(valueText)
        except:
            print("Invalid int value", valueText)
            value = oldValue
        self._displayInt(widget, value)
        return value

    def _displayReal(self, widget, value):
        newText = STRING_FLOAT_FORMAT.format(value)
        widget.setText(newText)

    def _parseReal(self, widget, oldValue):
        valueText = widget.text()
        try:
            value = float(valueText)
        except:
            print("Invalid real value", valueText)
            value = oldValue
        self._displayReal(widget, value)
        return value

    def _elementsAroundLineEditEntered(self):
        self._parseInt(self._ui.elementsAroundLineEdit, 12)

    def _elementsUpLineEditEntered(self):
        self._parseInt(self._ui.elementsUpLineEdit, 3)

    def _elementsAlongStemLineEditEntered(self):
        self._parseInt(self._ui.elementsAlongStemLineEdit, 1)

    #def _radiusLineEditEntered(self):
    #    self._parseReal(self._ui.radiusLineEdit, 1.0)

    #def _stemLengthLineEditEntered(self):
    #    self._parseReal(self._ui.stemLengthLineEdit, 0.5)
    

