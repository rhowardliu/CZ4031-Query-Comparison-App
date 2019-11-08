

def query_to_tree(query):
  return(query + ' tree')


self.pushButton.clicked.connect(self.onClickButton)

def onClickButton(self):
    query = self.plainTextEdit.toPlainText()
    tree = qp.query_to_tree(query)
    self.textBrowser.setText(tree)
    print(query)