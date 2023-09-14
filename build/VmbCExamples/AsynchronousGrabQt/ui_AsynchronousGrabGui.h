/********************************************************************************
** Form generated from reading UI file 'AsynchronousGrabGui.ui'
**
** Created by: Qt User Interface Compiler version 5.12.8
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ASYNCHRONOUSGRABGUI_H
#define UI_ASYNCHRONOUSGRABGUI_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTableView>
#include <QtWidgets/QTreeView>
#include <QtWidgets/QWidget>
#include <imagelabel.h>

QT_BEGIN_NAMESPACE

class Ui_AsynchronousGrabGui
{
public:
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    ImageLabel *m_renderLabel;
    QPushButton *m_acquisitionStartStopButton;
    QTreeView *m_cameraSelectionTree;
    QTableView *m_eventLog;

    void setupUi(QMainWindow *AsynchronousGrabGui)
    {
        if (AsynchronousGrabGui->objectName().isEmpty())
            AsynchronousGrabGui->setObjectName(QString::fromUtf8("AsynchronousGrabGui"));
        AsynchronousGrabGui->resize(1040, 780);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(AsynchronousGrabGui->sizePolicy().hasHeightForWidth());
        AsynchronousGrabGui->setSizePolicy(sizePolicy);
        AsynchronousGrabGui->setMinimumSize(QSize(1040, 780));
        AsynchronousGrabGui->setMaximumSize(QSize(16777215, 16777215));
        centralWidget = new QWidget(AsynchronousGrabGui);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        m_renderLabel = new ImageLabel(centralWidget);
        m_renderLabel->setObjectName(QString::fromUtf8("m_renderLabel"));
        m_renderLabel->setTextFormat(Qt::PlainText);
        m_renderLabel->setScaledContents(false);
        m_renderLabel->setAlignment(Qt::AlignCenter);

        gridLayout->addWidget(m_renderLabel, 0, 1, 1, 1);

        m_acquisitionStartStopButton = new QPushButton(centralWidget);
        m_acquisitionStartStopButton->setObjectName(QString::fromUtf8("m_acquisitionStartStopButton"));
        m_acquisitionStartStopButton->setEnabled(false);
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(m_acquisitionStartStopButton->sizePolicy().hasHeightForWidth());
        m_acquisitionStartStopButton->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(m_acquisitionStartStopButton, 1, 0, 1, 1);

        m_cameraSelectionTree = new QTreeView(centralWidget);
        m_cameraSelectionTree->setObjectName(QString::fromUtf8("m_cameraSelectionTree"));
        m_cameraSelectionTree->setEnabled(false);
        m_cameraSelectionTree->setRootIsDecorated(true);
        m_cameraSelectionTree->header()->setVisible(false);
        m_cameraSelectionTree->header()->setDefaultSectionSize(35);

        gridLayout->addWidget(m_cameraSelectionTree, 0, 0, 1, 1);

        m_eventLog = new QTableView(centralWidget);
        m_eventLog->setObjectName(QString::fromUtf8("m_eventLog"));
        QSizePolicy sizePolicy2(QSizePolicy::Expanding, QSizePolicy::Fixed);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(m_eventLog->sizePolicy().hasHeightForWidth());
        m_eventLog->setSizePolicy(sizePolicy2);
        m_eventLog->setEditTriggers(QAbstractItemView::NoEditTriggers);
        m_eventLog->setProperty("showDropIndicator", QVariant(false));
        m_eventLog->setSelectionMode(QAbstractItemView::SingleSelection);
        m_eventLog->setSelectionBehavior(QAbstractItemView::SelectRows);
        m_eventLog->setShowGrid(true);
        m_eventLog->horizontalHeader()->setHighlightSections(false);
        m_eventLog->horizontalHeader()->setStretchLastSection(true);
        m_eventLog->verticalHeader()->setVisible(false);

        gridLayout->addWidget(m_eventLog, 1, 1, 1, 1);

        gridLayout->setRowStretch(0, 1);
        gridLayout->setColumnStretch(1, 1);
        gridLayout->setColumnMinimumWidth(0, 300);
        gridLayout->setRowMinimumHeight(1, 100);
        AsynchronousGrabGui->setCentralWidget(centralWidget);

        retranslateUi(AsynchronousGrabGui);

        QMetaObject::connectSlotsByName(AsynchronousGrabGui);
    } // setupUi

    void retranslateUi(QMainWindow *AsynchronousGrabGui)
    {
        AsynchronousGrabGui->setWindowTitle(QApplication::translate("AsynchronousGrabGui", "Vmb C AsynchronousGrab", nullptr));
        m_renderLabel->setText(QString());
        m_acquisitionStartStopButton->setText(QApplication::translate("AsynchronousGrabGui", "Start Acquisition", nullptr));
    } // retranslateUi

};

namespace Ui {
    class AsynchronousGrabGui: public Ui_AsynchronousGrabGui {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ASYNCHRONOUSGRABGUI_H
